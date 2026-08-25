import json
from typing import Dict


class RemediationAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate(
        self,
        objective: str,
        risk_analysis: Dict,
        conflict_analysis: Dict,
        gap_analysis: Dict,
    ) -> Dict:

        prompt = f"""
You are an Enterprise Security Remediation Agent.

OBJECTIVE:
{objective}

RISK ANALYSIS:
{risk_analysis}

CONFLICT ANALYSIS:
{conflict_analysis}

KNOWLEDGE GAPS:
{gap_analysis}

Generate practical remediation actions.

Return ONLY valid JSON:

{{
  "remediations": [
    {{
      "issue": "...",
      "type": "risk|conflict|gap",
      "priority": "CRITICAL|HIGH|MEDIUM|LOW",
      "recommended_action": "...",
      "reason": "...",
      "suggested_owner": "...",
      "verification": "..."
    }}
  ],
  "summary": "..."
}}
"""

        response = self.llm.generate(
            question="Generate enterprise remediation actions.",
            context=prompt,
        )

        # Gemini unavailable -> deterministic fallback
        if self._llm_unavailable(response):
            return self._fallback(
                risk_analysis,
                conflict_analysis,
                gap_analysis,
            )

        parsed = self._parse_response(response)

        if not parsed.get("remediations"):
            return self._fallback(
                risk_analysis,
                conflict_analysis,
                gap_analysis,
            )

        return parsed

    def _llm_unavailable(self, response: str) -> bool:

        text = response.lower()

        return (
            "quota temporarily exceeded" in text
            or "ai generation service is temporarily unavailable"
            in text
            or "resource_exhausted" in text
        )

    def _fallback(
        self,
        risk_analysis: Dict,
        conflict_analysis: Dict,
        gap_analysis: Dict,
    ) -> Dict:

        remediations = []

        for risk in risk_analysis.get("risks", []):

            severity = str(
                risk.get("severity", "Medium")
            ).upper()

            priority_map = {
                "CRITICAL": "CRITICAL",
                "HIGH": "HIGH",
                "MEDIUM": "MEDIUM",
                "LOW": "LOW",
            }

            priority = priority_map.get(
                severity,
                "MEDIUM",
            )

            remediations.append({
                "issue": risk.get(
                    "title",
                    "Identified security risk",
                ),
                "type": "risk",
                "priority": priority,
                "recommended_action": risk.get(
                    "recommendation",
                    "Review and remediate the identified risk.",
                ),
                "reason": risk.get(
                    "impact",
                    "The issue was identified from enterprise evidence.",
                ),
                "suggested_owner": (
                    "Security / Risk Management"
                ),
                "verification": (
                    "Verify that the recommended control "
                    "has been implemented and re-evaluate "
                    "the related evidence."
                ),
            })

        for conflict in conflict_analysis.get(
            "conflicts",
            [],
        ):

            severity = str(
                conflict.get("severity", "Medium")
            ).upper()

            remediations.append({
                "issue": conflict.get(
                    "title",
                    "Policy conflict",
                ),
                "type": "conflict",
                "priority": (
                    severity
                    if severity in {
                        "CRITICAL",
                        "HIGH",
                        "MEDIUM",
                        "LOW",
                    }
                    else "MEDIUM"
                ),
                "recommended_action": (
                    "Review the conflicting policy requirements "
                    "and establish a single approved control."
                ),
                "reason": conflict.get(
                    "description",
                    "Conflicting requirements were identified "
                    "in enterprise evidence.",
                ),
                "suggested_owner": (
                    "Governance / Compliance"
                ),
                "verification": (
                    "Confirm that the conflicting requirements "
                    "have been reconciled and documented."
                ),
            })

        for gap in gap_analysis.get(
            "gaps",
            [],
        ):

            importance = str(
                gap.get("importance", "Medium")
            ).upper()

            remediations.append({
                "issue": gap.get(
                    "title",
                    "Knowledge gap",
                ),
                "type": "gap",
                "priority": (
                    importance
                    if importance in {
                        "CRITICAL",
                        "HIGH",
                        "MEDIUM",
                        "LOW",
                    }
                    else "MEDIUM"
                ),
                "recommended_action": (
                    "Collect, document, and validate the "
                    "missing enterprise information."
                ),
                "reason": gap.get(
                    "description",
                    "Required information was not sufficiently "
                    "available in the knowledge base.",
                ),
                "suggested_owner": (
                    "Knowledge Management / Governance"
                ),
                "verification": (
                    "Confirm that the missing information "
                    "has been documented and indexed."
                ),
            })

        return {
            "status": "fallback",
            "remediations": remediations,
            "summary": (
                "Remediation actions were generated from the "
                "retrieved risk, conflict, and knowledge-gap "
                "analysis because the LLM was unavailable."
            ),
        }

    def _parse_response(self, response: str) -> Dict:

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
                    "Remediation response must be an object."
                )

            return result

        except Exception as error:

            return {
                "remediations": [],
                "summary": (
                    "The remediation agent could not "
                    "produce structured remediation actions."
                ),
                "error": str(error),
            }
