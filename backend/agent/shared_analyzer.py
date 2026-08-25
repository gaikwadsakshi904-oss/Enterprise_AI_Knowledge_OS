import json
from typing import Dict


class SharedAnalyzer:

    """
    Performs combined enterprise evidence analysis.

    Uses Gemini when available.
    Falls back to deterministic evidence-based
    analysis when Gemini is unavailable.
    """

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
                "conflicts": [],
                "gaps": [],
            }

        prompt = f"""
You are an Enterprise Security and Governance
Analysis Agent.

Analyze ONLY the provided enterprise knowledge-base
evidence.

OBJECTIVE:
{objective}

EVIDENCE:
{evidence}

Identify:

1. SECURITY / OPERATIONAL RISKS
2. POLICY CONFLICTS
3. KNOWLEDGE GAPS

Do not invent facts.

Return ONLY valid JSON:

{{
  "risks": [],
  "conflicts": [],
  "gaps": []
}}
"""

        response = self.llm.generate(
            question=objective,
            context=prompt,
        )

        response_lower = response.lower()

        if (
            "quota temporarily exceeded" in response_lower
            or "ai generation service is temporarily unavailable"
            in response_lower
        ):
            return self._fallback_analysis(
                objective,
                evidence,
            )

        return self._parse(response)

    # =====================================================
    # LOCAL FALLBACK
    # =====================================================

    def _fallback_analysis(
        self,
        objective: str,
        evidence: str,
    ) -> Dict:

        text = evidence.lower()

        risks = []
        conflicts = []
        gaps = []

        # -------------------------------------------------
        # ACL / ACCESS CONTROL
        # -------------------------------------------------

        if "acl" in text or "access control" in text:

            risks.append({
                "title": "Access Control Enforcement Risk",
                "category": "Access Control",
                "severity": "High",
                "evidence": (
                    "Retrieved evidence requires ACL filters "
                    "matching user credentials."
                ),
                "impact": (
                    "Incorrect ACL enforcement could expose "
                    "restricted enterprise knowledge."
                ),
                "recommendation": (
                    "Enforce ACL filtering before retrieval "
                    "results are returned to users."
                ),
            })

        # -------------------------------------------------
        # LEAST PRIVILEGE
        # -------------------------------------------------

        if (
            "least privilege" in text
            or "principle of least privilege" in text
        ):

            risks.append({
                "title": "Privilege Management Risk",
                "category": "Authorization",
                "severity": "High",
                "evidence": (
                    "Retrieved security guidance requires "
                    "services to follow least privilege."
                ),
                "impact": (
                    "Excessive service permissions could "
                    "increase the impact of a compromised service."
                ),
                "recommendation": (
                    "Review service permissions and enforce "
                    "least-privilege access."
                ),
            })

        # -------------------------------------------------
        # AUDIT / LOGGING
        # -------------------------------------------------

        if (
            "audit" in text
            or "retrieval logs" in text
            or "telemetry" in text
        ):

            risks.append({
                "title": "Audit Monitoring Risk",
                "category": "Compliance",
                "severity": "Medium",
                "evidence": (
                    "Retrieved policies require audits of "
                    "model outputs and retrieval logs."
                ),
                "impact": (
                    "Insufficient monitoring could make "
                    "security or compliance incidents harder "
                    "to detect and investigate."
                ),
                "recommendation": (
                    "Regularly review model-output and "
                    "retrieval-log telemetry."
                ),
            })

        # -------------------------------------------------
        # PROMPT INJECTION
        # -------------------------------------------------

        if "prompt injection" in text:

            risks.append({
                "title": "Prompt Injection Risk",
                "category": "AI Security",
                "severity": "High",
                "evidence": (
                    "Retrieved policy explicitly prohibits "
                    "prompt injection manipulation."
                ),
                "impact": (
                    "Prompt injection could manipulate AI "
                    "processing or retrieval behavior."
                ),
                "recommendation": (
                    "Add prompt-injection detection and "
                    "input validation controls."
                ),
            })

        # -------------------------------------------------
        # DATA CLASSIFICATION
        # -------------------------------------------------

        if (
            "public" in text
            and "internal" in text
            and "confidential" in text
            and "restricted" in text
        ):

            gaps.append({
                "title": "Data Classification Enforcement Details",
                "description": (
                    "The evidence defines Public, Internal, "
                    "Confidential, and Restricted classifications "
                    "but does not provide complete implementation "
                    "details for classification enforcement."
                ),
                "evidence": (
                    "Retrieved policy evidence defines four "
                    "data classification levels."
                ),
                "importance": "Medium",
            })

        # -------------------------------------------------
        # RETENTION
        # -------------------------------------------------

        if "retention" not in text:

            gaps.append({
                "title": "Retention Policy Information Gap",
                "description": (
                    "Retrieved evidence does not specify "
                    "complete retention requirements for "
                    "knowledge, embeddings, or retrieval logs."
                ),
                "evidence": (
                    "No explicit retention period was found "
                    "in the retrieved evidence."
                ),
                "importance": "Medium",
            })

        # -------------------------------------------------
        # INCIDENT RESPONSE
        # -------------------------------------------------

        if "incident response" not in text:

            gaps.append({
                "title": "Incident Response Information Gap",
                "description": (
                    "Retrieved evidence does not provide "
                    "a complete incident-response procedure "
                    "for AI knowledge-system security events."
                ),
                "evidence": (
                    "No explicit incident-response procedure "
                    "was found in the retrieved evidence."
                ),
                "importance": "Medium",
            })

        # -------------------------------------------------
        # POLICY CONFLICT CHECK
        # -------------------------------------------------

        if (
            "unauthorized data exfiltration" in text
            and "access" in text
        ):

            conflicts.append({
                "title": "Access Governance Requires Consistency",
                "description": (
                    "The policies require strict access controls "
                    "while also defining multiple data-classification "
                    "levels. The retrieved evidence does not establish "
                    "whether every classification is consistently "
                    "mapped to the ACL enforcement mechanism."
                ),
                "evidence": (
                    "Evidence references both data classification "
                    "and ACL enforcement."
                ),
                "severity": "Medium",
            })

        return {
            "status": "fallback_completed",
            "risks": risks,
            "conflicts": conflicts,
            "gaps": gaps,
            "message": (
                "Gemini was unavailable. Analysis was generated "
                "using evidence-based local fallback rules."
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
                    "Shared analysis must be a JSON object."
                )

            return {
                "status": "completed",
                "risks": result.get("risks", []),
                "conflicts": result.get("conflicts", []),
                "gaps": result.get("gaps", []),
            }

        except Exception as error:

            return {
                "status": "parse_error",
                "risks": [],
                "conflicts": [],
                "gaps": [],
                "error": str(error),
            }
