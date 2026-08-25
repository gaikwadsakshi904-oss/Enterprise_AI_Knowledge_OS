from typing import Dict


class ConflictDetector:

    def __init__(self, llm):
        self.llm = llm

    def analyze(
        self,
        objective: str,
        evidence: str,
    ) -> Dict:

        if not evidence.strip():

            return {
                "status": "no_evidence",
                "conflicts": [],
            }

        prompt = f"""
You are an Enterprise Policy Conflict Detection Agent.

Your job is to identify potential contradictions,
inconsistencies, or policy overlaps in the provided
enterprise knowledge-base evidence.

OBJECTIVE:
{objective}

EVIDENCE:
{evidence}

Compare statements from different documents.

Look specifically for:

1. Direct policy contradictions
2. Different access-control requirements
3. Different security requirements
4. Different retention requirements
5. Different compliance requirements
6. Conflicting responsibilities
7. Inconsistent technical requirements

IMPORTANT:

- Use ONLY the provided evidence.
- Do not invent policies.
- Do not assume two policies conflict merely because
  they discuss the same topic.
- If there is insufficient evidence, say so.

For every potential conflict return:

- title
- severity
- document_a
- statement_a
- document_b
- statement_b
- explanation
- recommendation

Return ONLY valid JSON:

{{
  "conflicts": [
    {{
      "title": "...",
      "severity": "High",
      "document_a": "...",
      "statement_a": "...",
      "document_b": "...",
      "statement_b": "...",
      "explanation": "...",
      "recommendation": "..."
    }}
  ]
}}

If no conflicts are supported:

{{"conflicts":[]}}
"""

        response = self.llm.generate(
            question=objective,
            context=prompt,
        )

        return self._parse(response)

    def _parse(self, response: str) -> Dict:

        import json

        try:

            cleaned = response.strip()

            if cleaned.startswith("```"):
                cleaned = (
                    cleaned
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            result = json.loads(cleaned)

            conflicts = result.get(
                "conflicts",
                [],
            )

            valid_conflicts = []

            for conflict in conflicts:

                if not isinstance(
                    conflict,
                    dict,
                ):
                    continue

                valid_conflicts.append(
                    {
                        "title": conflict.get(
                            "title",
                            "Potential policy conflict",
                        ),
                        "severity": conflict.get(
                            "severity",
                            "Medium",
                        ),
                        "document_a": conflict.get(
                            "document_a",
                            "Unknown",
                        ),
                        "statement_a": conflict.get(
                            "statement_a",
                            "",
                        ),
                        "document_b": conflict.get(
                            "document_b",
                            "Unknown",
                        ),
                        "statement_b": conflict.get(
                            "statement_b",
                            "",
                        ),
                        "explanation": conflict.get(
                            "explanation",
                            "",
                        ),
                        "recommendation": conflict.get(
                            "recommendation",
                            "",
                        ),
                    }
                )

            return {
                "status": "completed",
                "conflicts": valid_conflicts,
            }

        except Exception as error:

            return {
                "status": "parse_error",
                "conflicts": [],
                "error": str(error),
            }
