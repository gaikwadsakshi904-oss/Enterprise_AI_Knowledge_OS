from typing import Dict


class KnowledgeGapDetector:

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
                "gaps": [],
            }

        prompt = f"""
You are an Enterprise Knowledge Gap Detection Agent.

Analyze ONLY the provided enterprise knowledge-base
evidence.

OBJECTIVE:
{objective}

EVIDENCE:
{evidence}

Identify important information that appears to be
missing, incomplete, ambiguous, outdated, or insufficiently
specified.

Look for:

1. Missing policies
2. Missing procedures
3. Undefined responsibilities
4. Missing security controls
5. Missing compliance requirements
6. Missing technical specifications
7. Undefined thresholds or metrics
8. Incomplete incident-response information
9. Missing ownership or escalation paths
10. Important unanswered questions

IMPORTANT:

- Do not invent missing facts.
- A gap must be justified by the evidence.
- Distinguish between "not found in provided evidence"
  and "does not exist".
- Use only the supplied knowledge-base evidence.

For every gap return:

- title
- category
- severity
- evidence
- why_it_matters
- recommended_action

Return ONLY valid JSON:

{{
  "gaps": [
    {{
      "title": "...",
      "category": "...",
      "severity": "High",
      "evidence": "...",
      "why_it_matters": "...",
      "recommended_action": "..."
    }}
  ]
}}

If no meaningful gaps are supported:

{{"gaps":[]}}
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

            gaps = result.get(
                "gaps",
                [],
            )

            valid_gaps = []

            for gap in gaps:

                if not isinstance(
                    gap,
                    dict,
                ):
                    continue

                valid_gaps.append(
                    {
                        "title": gap.get(
                            "title",
                            "Knowledge gap",
                        ),
                        "category": gap.get(
                            "category",
                            "Unknown",
                        ),
                        "severity": gap.get(
                            "severity",
                            "Medium",
                        ),
                        "evidence": gap.get(
                            "evidence",
                            "",
                        ),
                        "why_it_matters": gap.get(
                            "why_it_matters",
                            "",
                        ),
                        "recommended_action": gap.get(
                            "recommended_action",
                            "",
                        ),
                    }
                )

            return {
                "status": "completed",
                "gaps": valid_gaps,
            }

        except Exception as error:

            return {
                "status": "parse_error",
                "gaps": [],
                "error": str(error),
            }
