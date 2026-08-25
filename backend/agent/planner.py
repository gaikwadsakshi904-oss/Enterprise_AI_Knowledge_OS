import json
from typing import Dict


class AgentPlanner:

    MAX_TASKS = 3

    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, objective: str) -> Dict:

        prompt = f"""
You are an Enterprise AI Research Planner.

Break the following enterprise research objective
into EXACTLY 3 focused research tasks.

OBJECTIVE:
{objective}

Return ONLY valid JSON with exactly this structure:

{{
  "objective": "{objective}",
  "tasks": [
    {{
      "id": 1,
      "title": "Evidence / policy discovery",
      "query": "Search query"
    }},
    {{
      "id": 2,
      "title": "Risk / conflict analysis",
      "query": "Search query"
    }},
    {{
      "id": 3,
      "title": "Knowledge gap analysis",
      "query": "Search query"
    }}
  ]
}}

Do not add markdown or explanations.
"""

        response = self.llm.generate(
            question=objective,
            context=prompt,
        )

        response_lower = str(response).lower()

        if (
            "quota temporarily exceeded" in response_lower
            or "generation service is temporarily unavailable" in response_lower
            or "ai generation service is temporarily unavailable" in response_lower
        ):
            return self._fallback(objective)

        return self._parse_plan(response, objective)

    def _fallback(self, objective: str) -> Dict:

        return {
            "objective": objective,
            "status": "fallback",
            "tasks": [
                {
                    "id": 1,
                    "title": "Find relevant policies",
                    "query": objective,
                },
                {
                    "id": 2,
                    "title": "Identify risks and conflicts",
                    "query": f"{objective} risks conflicts",
                },
                {
                    "id": 3,
                    "title": "Identify knowledge gaps",
                    "query": f"{objective} gaps missing information",
                },
            ],
        }

    def _parse_plan(self, response: str, objective: str) -> Dict:

        try:

            cleaned = str(response).strip()

            if cleaned.startswith("```"):
                cleaned = (
                    cleaned
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            plan = json.loads(cleaned)

            if not isinstance(plan, dict):
                raise ValueError("Plan must be an object.")

            raw_tasks = plan.get("tasks", [])

            if not isinstance(raw_tasks, list):
                raise ValueError("Tasks must be a list.")

            # IMPORTANT:
            # Only keep dictionary tasks.
            tasks = [
                task
                for task in raw_tasks
                if isinstance(task, dict)
                and isinstance(task.get("query"), str)
                and task.get("query", "").strip()
            ]

            if not tasks:
                raise ValueError("Planner returned no valid tasks.")

            normalized = []

            for index, task in enumerate(
                tasks[:self.MAX_TASKS],
                1,
            ):

                normalized.append(
                    {
                        "id": task.get("id", index),
                        "title": task.get(
                            "title",
                            f"Research Task {index}",
                        ),
                        "query": task.get(
                            "query",
                            objective,
                        ),
                    }
                )

            return {
                "objective": objective,
                "tasks": normalized,
            }

        except Exception:

            return self._fallback(objective)
