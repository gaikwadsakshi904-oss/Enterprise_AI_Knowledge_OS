from typing import Dict, List

from config import (
    TOP_K,
    MIN_RELEVANCE_SCORE,
)

from embedding import EmbeddingService
from vector_store import VectorStore
from llm import LLMService

from document_loader import load_documents
from hybrid_search import HybridSearch
from reranker import Reranker
from confidence import ConfidenceEngine


class RAGPipeline:

    def __init__(self):

        print("Initializing RAG Pipeline...")

        # =================================================
        # EMBEDDING
        # =================================================

        self.embedding_service = EmbeddingService()

        # =================================================
        # VECTOR STORE
        # =================================================

        self.vector_store = VectorStore()

        try:

            self.vector_store.load()

            print(
                f"FAISS index loaded: "
                f"{self.vector_store.count()} vectors"
            )

        except Exception as e:

            print(
                f"Warning: Could not load FAISS index: {e}"
            )

        # =================================================
        # DOCUMENTS
        # =================================================

        try:

            from config import DOCUMENTS_DIR

            self.chunks = load_documents(
                DOCUMENTS_DIR
            )

            print(
                f"Knowledge chunks loaded: "
                f"{len(self.chunks)}"
            )

        except Exception as e:

            print(
                f"Warning: Could not load documents: {e}"
            )

            self.chunks = []

        # =================================================
        # HYBRID SEARCH
        # =================================================

        if self.chunks:

            self.hybrid_search = HybridSearch(
                chunks=self.chunks,
                embedding_service=self.embedding_service,
                vector_store=self.vector_store
            )

            print(
                "Hybrid Search ready."
            )

        else:

            self.hybrid_search = None

        # =================================================
        # RERANKER
        # =================================================

        if self.hybrid_search:

            self.reranker = Reranker(
                self.embedding_service
            )

            print(
                "Reranker ready."
            )

        else:

            self.reranker = None

        # =================================================
        # CONFIDENCE ENGINE
        # =================================================

        self.confidence_engine = (
            ConfidenceEngine()
        )

        print(
            "Confidence Engine ready."
        )

        # =================================================
        # LLM
        # =================================================

        self.llm = LLMService()

        print(
            "RAG Pipeline ready."
        )

    # =====================================================
    # RETRIEVE
    # =====================================================

    def retrieve(
        self,
        question: str,
        top_k: int = TOP_K,
    ) -> List[Dict]:

        if self.hybrid_search is None:

            return []

        # -------------------------------------------------
        # Hybrid retrieval
        # -------------------------------------------------

        hybrid_results = (
            self.hybrid_search.search(
                query=question,
                top_k=max(
                    top_k * 2,
                    10
                ),
            )
        )

        if not hybrid_results:

            return []

        # -------------------------------------------------
        # Reranking
        # -------------------------------------------------

        reranked_results = (
            self.reranker.rerank(
                query=question,
                results=hybrid_results,
                top_k=top_k,
            )
        )

        # -------------------------------------------------
        # Convert results
        # -------------------------------------------------

        final_results = []

        for result in reranked_results:

            chunk = result["chunk"]

            if isinstance(chunk, dict):

                text = chunk.get(
                    "text",
                    ""
                )

                document = (
                    chunk.get("document")
                    or chunk.get("source")
                    or "Unknown"
                )

                page = chunk.get(
                    "page"
                )

                chunk_id = chunk.get(
                    "chunk_id"
                )

            else:

                text = getattr(
                    chunk,
                    "text",
                    ""
                )

                document = (
                    getattr(
                        chunk,
                        "document",
                        None
                    )
                    or getattr(
                        chunk,
                        "source",
                        "Unknown"
                    )
                )

                page = getattr(
                    chunk,
                    "page",
                    None
                )

                chunk_id = getattr(
                    chunk,
                    "chunk_id",
                    None
                )

            reranker_score = float(
                result.get(
                    "reranker_score",
                    result.get(
                        "score",
                        0.0
                    )
                )
            )

            if (
                reranker_score
                < MIN_RELEVANCE_SCORE
            ):

                continue

            final_results.append({

                "document": document,

                "page": page,

                "score": reranker_score,

                "chunk_id": (
                    chunk_id
                    if chunk_id is not None
                    else str(
                        result.get(
                            "index",
                            len(final_results)
                        )
                    )
                ),

                "text": text,

                "hybrid_score": float(
                    result.get(
                        "hybrid_score",
                        0.0
                    )
                ),

                "semantic_score": float(
                    result.get(
                        "semantic_score",
                        0.0
                    )
                ),

                "keyword_score": float(
                    result.get(
                        "keyword_score",
                        0.0
                    )
                ),

                "reranker_score": reranker_score,
            })

        return final_results

    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    def build_context(
        self,
        results: List[Dict],
    ) -> str:

        context_parts = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            source = result[
                "document"
            ]

            page = result.get(
                "page"
            )

            if page is not None:

                source_info = (
                    f"{source}, page {page}"
                )

            else:

                source_info = source

            context_parts.append(
                f"""
SOURCE {index}
Document: {source_info}
Relevance: {result['score']:.4f}
Hybrid Score: {result.get('hybrid_score', 0.0):.4f}
Reranker Score: {result.get('reranker_score', 0.0):.4f}

Content:
{result['text']}
"""
            )

        return "\n".join(
            context_parts
        )

    # =====================================================
    # ASK
    # =====================================================

    def ask(
        self,
        question: str,
    ) -> Dict:

        question = question.strip()

        if not question:

            return {
                "answer": (
                    "Please provide a question."
                ),
                "sources": [],
                "confidence": {
                    "score": 0.0,
                    "percentage": 0.0,
                    "level": "LOW",
                    "grounded": False,
                },
            }

        # =================================================
        # RETRIEVE
        # =================================================

        results = self.retrieve(
            question
        )

        # =================================================
        # CONFIDENCE
        # =================================================

        confidence = (
            self.confidence_engine.calculate(
                results
            )
        )

        print(
            f"Confidence: "
            f"{confidence['percentage']}% "
            f"({confidence['level']})"
        )

        # =================================================
        # GROUNDING GUARD
        # =================================================

        if not results:

            return {

                "answer": (
                    "I could not find relevant "
                    "information in the knowledge base."
                ),

                "sources": [],

                "confidence": confidence,

            }

        if not confidence["grounded"]:

            return {

                "answer": (
                    "I could not find enough reliable "
                    "evidence in the enterprise knowledge "
                    "base to answer this question confidently."
                ),

                "sources": [
                    {
                        "document": result[
                            "document"
                        ],

                        "page": result.get(
                            "page"
                        ),

                        "score": result[
                            "score"
                        ],

                        "chunk_id": result[
                            "chunk_id"
                        ],

                    }

                    for result in results
                ],

                "confidence": confidence,

            }

        # =================================================
        # BUILD CONTEXT
        # =================================================

        context = self.build_context(
            results
        )

        # =================================================
        # GENERATE ANSWER
        # =================================================

        answer = self.llm.generate(
            question=question,
            context=context,
        )

        # =================================================
        # SOURCES
        # =================================================

        sources = []

        for result in results:

            sources.append({

                "document": result[
                    "document"
                ],

                "page": result.get(
                    "page"
                ),

                "score": result[
                    "score"
                ],

                "chunk_id": result[
                    "chunk_id"
                ],

                "hybrid_score": result.get(
                    "hybrid_score",
                    0.0
                ),

                "reranker_score": result.get(
                    "reranker_score",
                    0.0
                ),

            })

        # =================================================
        # FINAL RESPONSE
        # =================================================

        return {

            "answer": answer,

            "sources": sources,

            "confidence": confidence,

        }
