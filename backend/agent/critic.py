import json
from typing import Dict


class AgentCritic:

    def __init__(self, llm):
        self.llm = llm

    def verify(
        self,
        objective: str,
        evidence: str,
        risk_analysis: Dict,
        conflict_analysis: Dict,
        gap_analysis: Dict,
    ) -> Dict:

        if not evidence.strip():

            return {
                "overall_status": "no_evidence",
                "verified_risks": [],
                "verified_conflicts": [],
                "verified_gaps": [],
                "rejected_findings": [],
                "verification_summary": (
                    "No evidence was available for verification."
                ),
            }

        prompt = f"""
You are the verification and quality-control agent
for an Enterprise AI Knowledge OS.

Verify whether the following conclusions are supported
by the provided enterprise evidence.

OBJECTIVE:
{objective}

EVIDENCE:
{evidence}

RISK ANALYSIS:
{risk_analysis}

CONFLICT ANALYSIS:
{conflict_analysis}

KNOWLEDGE GAP ANALYSIS:
{gap_analysis}

Use only the provided evidence.

Verdicts:

SUPPORTED
PARTIALLY_SUPPORTED
UNSUPPORTED

Return ONLY valid JSON:

{{
  "overall_status": "verified",
  "verified_risks": [],
  "verified_conflicts": [],
  "verified_gaps": [],
  "rejected_findings": [],
  "verification_summary": "..."
}}
"""

        response = self.llm.generate(
            question=objective,
            context=prompt,
        )

        if self._llm_unavailable(response):

            return self._fallback_verify(
                evidence,
                risk_analysis,
                conflict_analysis,
                gap_analysis,
            )

        return self._parse(response)

    # =====================================================
    # LLM UNAVAILABLE DETECTION
    # =====================================================

    def _llm_unavailable(self, response: str) -> bool:

        text = response.lower()

        return (
            "quota temporarily exceeded" in text
            or "resource_exhausted" in text
            or "ai generation service is temporarily unavailable"
            in text
            or "generation service is temporarily unavailable"
            in text
        )

    # =====================================================
    # DETERMINISTIC FALLBACK VERIFICATION
    # =====================================================

    def _fallback_verify(
        self,
        evidence: str,
        risk_analysis: Dict,
        conflict_analysis: Dict,
        gap_analysis: Dict,
    ) -> Dict:

        verified_risks = []
        verified_conflicts = []
        verified_gaps = []
        rejected_findings = []

        evidence_lower = evidence.lower()

        # -------------------------------------------------
        # RISKS
        # -------------------------------------------------

        for risk in risk_analysis.get("risks", []):

            title = risk.get(
                "title",
                "Unnamed risk",
            )

            risk_evidence = str(
                risk.get(
                    "evidence",
                    "",
                )
            ).strip()

            if risk_evidence:

                verified_risks.append({
                    "title": title,
                    "verdict": "SUPPORTED",
                    "reason": (
                        "The risk contains supporting evidence "
                        "from the enterprise analysis."
                    ),
                    "evidence": risk_evidence,
                })

            elif title.lower() in evidence_lower:

                verified_risks.append({
                    "title": title,
                    "verdict": "SUPPORTED",
                    "reason": (
                        "The risk title is directly represented "
                        "in the retrieved enterprise evidence."
                    ),
                    "evidence": title,
                })

            else:

                rejected_findings.append({
                    "title": title,
                    "type": "risk",
                    "verdict": "UNSUPPORTED",
                    "reason": (
                        "No direct supporting evidence was "
                        "available for this finding."
                    ),
                })

        # -------------------------------------------------
        # CONFLICTS
        # -------------------------------------------------

        for conflict in conflict_analysis.get(
            "conflicts",
            [],
        ):

            title = conflict.get(
                "title",
                "Unnamed conflict",
            )

            conflict_evidence = str(
                conflict.get(
                    "evidence",
                    "",
                )
            ).strip()

            if conflict_evidence:

                verified_conflicts.append({
                    "title": title,
                    "verdict": "SUPPORTED",
                    "reason": (
                        "The conflict contains supporting "
                        "enterprise evidence."
                    ),
                    "evidence": conflict_evidence,
                })

            elif title.lower() in evidence_lower:

                verified_conflicts.append({
                    "title": title,
                    "verdict": "SUPPORTED",
                    "reason": (
                        "The conflict title is represented "
                        "in the retrieved evidence."
                    ),
                    "evidence": title,
                })

            else:

                rejected_findings.append({
                    "title": title,
                    "type": "conflict",
                    "verdict": "UNSUPPORTED",
                    "reason": (
                        "No direct supporting evidence was "
                        "available for this conflict."
                    ),
                })

        # -------------------------------------------------
        # KNOWLEDGE GAPS
        # -------------------------------------------------

        for gap in gap_analysis.get(
            "gaps",
            [],
        ):

            title = gap.get(
                "title",
                "Unnamed knowledge gap",
            )

            gap_evidence = str(
                gap.get(
                    "evidence",
                    "",
                )
            ).strip()

            if gap_evidence:

                verified_gaps.append({
                    "title": title,
                    "verdict": "SUPPORTED",
                    "reason": (
                        "The knowledge gap contains supporting "
                        "enterprise evidence."
                    ),
                    "evidence": gap_evidence,
                })

            elif title.lower() in evidence_lower:

                verified_gaps.append({
                    "title": title,
                    "verdict": "SUPPORTED",
                    "reason": (
                        "The gap is represented in the "
                        "retrieved enterprise evidence."
                    ),
                    "evidence": title,
                })

            else:

                rejected_findings.append({
                    "title": title,
                    "type": "gap",
                    "verdict": "UNSUPPORTED",
                    "reason": (
                        "No direct supporting evidence was "
                        "available for this gap."
                    ),
                })

        total_verified = (
            len(verified_risks)
            + len(verified_conflicts)
            + len(verified_gaps)
        )

        total_rejected = len(
            rejected_findings
        )

        if total_rejected == 0:

            overall_status = "verified"

        elif total_verified > 0:

            overall_status = "partially_verified"

        else:

            overall_status = "verification_failed"

        return {
            "overall_status": overall_status,
            "verified_risks": verified_risks,
            "verified_conflicts": verified_conflicts,
            "verified_gaps": verified_gaps,
            "rejected_findings": rejected_findings,
            "verification_summary": (
                f"Evidence-based fallback verification completed. "
                f"{total_verified} findings were supported and "
                f"{total_rejected} findings were rejected."
            ),
            "verification_method": (
                "deterministic_evidence_fallback"
            ),
        }

    # =====================================================
    # JSON PARSER
    # =====================================================

    def _parse(self, response: str) -> Dict:

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
                    "Verification result must be a JSON object."
                )

            return {
                "overall_status": result.get(
                    "overall_status",
                    "verified",
                ),
                "verified_risks": result.get(
                    "verified_risks",
                    [],
                ),
                "verified_conflicts": result.get(
                    "verified_conflicts",
                    [],
                ),
                "verified_gaps": result.get(
                    "verified_gaps",
                    [],
                ),
                "rejected_findings": result.get(
                    "rejected_findings",
                    [],
                ),
                "verification_summary": result.get(
                    "verification_summary",
                    "",
                ),
            }

        except Exception as error:

            return {
                "overall_status": "verification_error",
                "verified_risks": [],
                "verified_conflicts": [],
                "verified_gaps": [],
                "rejected_findings": [],
                "verification_summary": (
                    "Verification could not be completed."
                ),
                "error": str(error),
            }
