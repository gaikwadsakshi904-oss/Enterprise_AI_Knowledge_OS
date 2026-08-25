from document_loader import load_documents
from embedding import EmbeddingService
from vector_store import VectorStore
from hybrid_search import HybridSearch
from reranker import Reranker
from config import DOCUMENTS_DIR


def get_text(chunk):

    if isinstance(chunk, dict):
        return chunk.get("text", "")

    return getattr(
        chunk,
        "text",
        ""
    )


def get_source(chunk):

    if isinstance(chunk, dict):

        return (
            chunk.get("source")
            or chunk.get("document")
            or "Unknown"
        )

    return getattr(
        chunk,
        "source",
        "Unknown"
    )


def main():

    print("=" * 70)
    print("ENTERPRISE AI KNOWLEDGE OS")
    print("HYBRID SEARCH + RERANKER TEST")
    print("=" * 70)

    print("\n[1/5] Loading documents...")

    chunks = load_documents(
        DOCUMENTS_DIR
    )

    print(
        f"Loaded chunks: {len(chunks)}"
    )

    print("\n[2/5] Loading embedding service...")

    embedding_service = EmbeddingService()

    print("\n[3/5] Loading vector store...")

    vector_store = VectorStore()
    vector_store.load()

    print(
        f"Vector index: "
        f"{vector_store.count()} vectors"
    )

    print("\n[4/5] Initializing retrieval...")

    hybrid = HybridSearch(
        chunks=chunks,
        embedding_service=embedding_service,
        vector_store=vector_store
    )

    reranker = Reranker(
        embedding_service
    )

    print("Hybrid search + reranker ready.")

    print("\n[5/5] Starting test...")

    while True:

        query = input(
            "\nAsk a question "
            "(type 'exit' to quit): "
        ).strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        # First stage
        hybrid_results = hybrid.search(
            query=query,
            top_k=10
        )

        print(
            f"\nHybrid candidates: "
            f"{len(hybrid_results)}"
        )

        # Second stage
        final_results = reranker.rerank(
            query=query,
            results=hybrid_results,
            top_k=5
        )

        print("\n" + "=" * 70)
        print("RERANKED RESULTS")
        print("=" * 70)

        for i, result in enumerate(
            final_results,
            start=1
        ):

            chunk = result["chunk"]

            print(f"\n#{i}")

            print(
                f"Source: "
                f"{get_source(chunk)}"
            )

            print(
                f"Hybrid Score: "
                f"{result['hybrid_score']:.4f}"
            )

            print(
                f"Reranker Score: "
                f"{result['reranker_score']:.4f}"
            )

            print(
                f"\n{get_text(chunk)[:700]}"
            )

            print("-" * 70)


if __name__ == "__main__":
    main()
