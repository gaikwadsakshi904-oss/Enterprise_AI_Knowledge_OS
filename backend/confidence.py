from typing import Dict, List

from config import (
    CONFIDENCE_HIGH,
    CONFIDENCE_MEDIUM,
    MIN_EVIDENCE_SCORE,
)


class ConfidenceEngine:

    def calculate(
        self,
        results: List[Dict],
    ) -> Dict:

        if not results:

            return {
                "score": 0.0,
                "percentage": 0.0,
                "level": "LOW",
                "grounded": False,
                "best_evidence": 0.0,
                "average_evidence": 0.0,
                "evidence_coverage": 0.0,
                "reason": (
                    "No relevant evidence "
                    "was retrieved."
                ),
            }

        scores = [
            float(
                result.get(
                    "reranker_score",
                    result.get(
                        "score",
                        0.0
                    )
                )
            )
            for result in results
        ]

        best_score = max(scores)

        average_score = (
            sum(scores) / len(scores)
        )

        evidence_count = sum(
            1
            for score in scores
            if score >= MIN_EVIDENCE_SCORE
        )

        evidence_coverage = (
            evidence_count / len(scores)
        )

        confidence = (
            best_score * 0.60
            + average_score * 0.25
            + evidence_coverage * 0.15
        )

        confidence = max(
            0.0,
            min(confidence, 1.0)
        )

        if confidence >= CONFIDENCE_HIGH:

            level = "HIGH"
            grounded = True

            reason = (
                "Strong evidence was retrieved "
                "from the knowledge base."
            )

        elif confidence >= CONFIDENCE_MEDIUM:

            level = "MEDIUM"
            grounded = True

            reason = (
                "Moderate evidence was retrieved. "
                "The answer should be interpreted "
                "with some caution."
            )

        else:

            level = "LOW"
            grounded = False

            reason = (
                "The retrieved evidence is too weak "
                "to confidently ground an answer."
            )

        return {

            "score": round(
                confidence,
                4
            ),

            "percentage": round(
                confidence * 100,
                2
            ),

            "level": level,

            "grounded": grounded,

            "best_evidence": round(
                best_score,
                4
            ),

            "average_evidence": round(
                average_score,
                4
            ),

            "evidence_coverage": round(
                evidence_coverage,
                4
            ),

            "reason": reason,
        }
