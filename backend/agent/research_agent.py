from typing import Dict

class ResearchAgent:

    def __init__(self, rag_pipeline):
        self.rag = rag_pipeline

    def investigate(self, objective: str, top_k: int = 8) -> Dict:

        results = self.rag.retrieve(
            objective,
            top_k=top_k,
        )

        if not results:
            return {
                "objective": objective,
                "status": "no_evidence",
                "findings": [],
                "sources": [],
                "context": "",
            }

        context_parts = []

        for i, result in enumerate(results, 1):
            context_parts.append(
                f"""
SOURCE {i}
Document: {result.get("document", "Unknown")}
Page: {result.get("page", "N/A")}
Retrieval Score: {result.get("score", 0)}

CONTENT:
{result.get("text", "")}
"""
            )

        context = "\n".join(context_parts)

        return {
            "objective": objective,
            "status": "evidence_found",
            "findings": results,
            "sources": [
                {
                    "document": r.get("document", "Unknown"),
                    "page": r.get("page"),
                    "score": float(r.get("score", 0)),
                }
                for r in results
            ],
            "context": context,
        }

    def generate_report(self, objective: str, context: str) -> str:

        prompt = f"""
You are an Enterprise Research Agent.

Your job is to analyze enterprise knowledge-base evidence
and produce a useful research report.

OBJECTIVE:
{objective}

EVIDENCE:
{context}

Rules:

1. Use ONLY the provided evidence.
2. Never invent enterprise facts.
3. Clearly distinguish evidence from recommendations.
4. Identify risks or conflicts only when supported.
5. Mention when evidence is insufficient.
6. Be concise but detailed enough for an enterprise user.

Return the report using this structure:

EXECUTIVE SUMMARY

KEY FINDINGS

RISKS / CONFLICTS

KNOWLEDGE GAPS

RECOMMENDATIONS

EVIDENCE SOURCES
"""

        return self.rag.llm.generate(
            question=objective,
            context=prompt,
        )
