from typing import Dict, List


class RiskAnalyzer:

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
                "risks": [],
            }

        prompt = f"""
You are an Enterprise Cyber Risk Analysis Agent.

Analyze ONLY the provided enterprise knowledge-base evidence.

OBJECTIVE:
{objective}

EVIDENCE:
{evidence}

Identify security, compliance, operational, privacy,
governance, and AI risks that are actually supported
by the evidence.

For every risk provide:

- title
- category
- severity: Critical, High, Medium, or Low
- evidence
- impact
- recommendation

Do not invent facts.

Return ONLY valid JSON:

{{
  "risks": [
    {{
      "title": "...",
      "category": "...",
      "severity": "...",
      "evidence": "...",
      "impact": "...",
      "recommendation": "..."
    }}
  ]
}}

If no risks are supported, return:

{{"risks":[]}}
"""

        response = self.llm.generate(
            question=objective,
            context=prompt,
        )

        # LLM service may return a quota/unavailable message.
        response_lower = response.lower()

        if (
            "quota temporarily exceeded" in response_lower
            or "ai generation service is temporarily unavailable"
            in response_lower
        ):

            return {
                "status": "llm_unavailable",
                "risks": [],
                "message": response,
            }

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

            if not isinstance(result, dict):
                raise ValueError(
                    "Risk analysis must be a JSON object."
                )

            risks = result.get(
                "risks",
                [],
            )

            valid_risks: List[Dict] = []

            for risk in risks:

                if not isinstance(risk, dict):
                    continue

                valid_risks.append(
                    {
                        "title": risk.get(
                            "title",
                            "Unnamed risk",
                        ),
                        "category": risk.get(
                            "category",
                            "Unknown",
                        ),
                        "severity": risk.get(
                            "severity",
                            "Medium",
                        ),
                        "evidence": risk.get(
                            "evidence",
                            "",
                        ),
                        "impact": risk.get(
                            "impact",
                            "",
                        ),
                        "recommendation": risk.get(
                            "recommendation",
                            "",
                        ),
                    }
                )

            return {
                "status": "completed",
                "risks": valid_risks,
            }

        except Exception as error:

            return {
                "status": "parse_error",
                "risks": [],
                "error": str(error),
            }
