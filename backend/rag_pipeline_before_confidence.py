from typing import Dict, List

from config import TOP_K, MIN_RELEVANCE_SCORE
from embedding import EmbeddingService
from vector_store import VectorStore
from llm import LLMService

from document_loader import load_documents
from hybrid_search import HybridSearch
from reranker import Reranker


class RAGPipeline:

    def __init__(self):

        print("Initializing RAG Pipeline...")

        # -------------------------------------------------
        # Embedding service
        # -------------------------------------------------

        self.embedding_service = (
            EmbeddingService()
        )

        # -------------------------------------------------
        # Vector store
        # -------------------------------------------------

        self.vector_store = (
            VectorStore()
        )

        # Load existing FAISS index
        try:
            self.vector_store.load()

            print(
                f"FAISS index loaded: "
                f"{self.vector_store.count()} vectors"
            )

        except Exception as e:

            print(
                "Warning: Could not load "
                f"FAISS index: {e}"
            )

        # -------------------------------------------------
        # Load document chunks
        # -------------------------------------------------

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
                "Warning: Could not load "
                f"document chunks: {e}"
            )

            self.chunks = []

        # -------------------------------------------------
        # Hybrid search
        # -------------------------------------------------

        if self.chunks:

            self.hybrid_search = HybridSearch(
                chunks=self.chunks,
                embedding_service=self.embedding_service,
                vector_store=self.vector_store
            )

            # -------------------------------------------------
            # Reranker
            # -------------------------------------------------

            self.reranker = Reranker(
                self.embedding_service
            )

            print(
                "Hybrid Search + Reranker ready."
            )

        else:

            self.hybrid_search = None
            self.reranker = None

        # -------------------------------------------------
        # LLM
        # -------------------------------------------------

        self.llm = (
            LLMService()
        )

        print("RAG Pipeline ready.")

    # =====================================================
    # RETRIEVE
    # =====================================================

    def retrieve(
        self,
        question: str,
        top_k: int = TOP_K,
    ) -> List[Dict]:

        # -------------------------------------------------
        # Hybrid retrieval
        # -------------------------------------------------

        if self.hybrid_search is None:

            return []

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
        # Convert result format
        # back to existing RAG format
        # -------------------------------------------------

        final_results = []

        for result in reranked_results:

            chunk = result["chunk"]

            # ---------------------------------------------
            # Extract metadata
            # ---------------------------------------------

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
                    or
                    getattr(
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

            # ---------------------------------------------
            # Relevance score
            #
            # Reranker score is now the primary
            # relevance score.
            # ---------------------------------------------

            relevance_score = float(
                result.get(
                    "reranker_score",
                    result.get(
                        "hybrid_score",
                        0.0
                    )
                )
            )

            # ---------------------------------------------
            # Minimum relevance filtering
            # ---------------------------------------------

            if (
                relevance_score
                < MIN_RELEVANCE_SCORE
            ):

                continue

            final_results.append({

                "document": document,

                "page": page,

                "score": relevance_score,

                "chunk_id": (
                    chunk_id
                    if chunk_id is not None
                    else str(
                        result["index"]
                    )
                ),

                "text": text,

                # Additional retrieval
                # diagnostics
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

                "reranker_score": relevance_score,
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
            }

        # -------------------------------------------------
        # Retrieve
        # -------------------------------------------------

        results = self.retrieve(
            question
        )

        if not results:

            return {
                "answer": (
                    "I could not find relevant "
                    "information in the knowledge base."
                ),
                "sources": [],
            }

        # -------------------------------------------------
        # Build context
        # -------------------------------------------------

        context = self.build_context(
            results
        )

        # -------------------------------------------------
        # Generate answer
        # -------------------------------------------------

        answer = self.llm.generate(
            question=question,
            context=context,
        )

        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return {

            "answer": answer,

            "sources": sources,

        }
