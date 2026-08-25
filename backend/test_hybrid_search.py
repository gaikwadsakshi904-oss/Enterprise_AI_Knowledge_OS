from document_loader import load_documents
from embedding import EmbeddingService
from vector_store import VectorStore
from hybrid_search import HybridSearch
from config import DOCUMENTS_DIR


def main():

    print("=" * 60)
    print("ENTERPRISE AI KNOWLEDGE OS")
    print("HYBRID SEARCH TEST")
    print("=" * 60)

    print("\n[1/4] Loading documents...")

    chunks = load_documents(DOCUMENTS_DIR)

    print(f"Loaded chunks: {len(chunks)}")

    print("\n[2/4] Loading embedding service...")

    embedding_service = EmbeddingService()

    print("\n[3/4] Loading vector store...")

    vector_store = VectorStore()
    vector_store.load()

    print(f"Vector index loaded: {vector_store.count()} vectors")

    print("\n[4/4] Creating hybrid search engine...")

    hybrid = HybridSearch(
        chunks=chunks,
        embedding_service=embedding_service,
        vector_store=vector_store
    )

    print("Hybrid search ready.")

    while True:

        query = input(
            "\nEnter your question "
            "(type 'exit' to quit): "
        ).strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        results = hybrid.search(
            query=query,
            top_k=5
        )

        print("\n" + "=" * 60)
        print("HYBRID SEARCH RESULTS")
        print("=" * 60)

        for i, result in enumerate(results, start=1):

            print(f"\n#{i}")

            print(
                f"Hybrid Score: "
                f"{result['hybrid_score']:.4f}"
            )

            print(
                f"Semantic Score: "
                f"{result['semantic_score']:.4f}"
            )

            print(
                f"Keyword Score: "
                f"{result['keyword_score']:.4f}"
            )

            chunk = result["chunk"]

            if isinstance(chunk, dict):

                text = chunk.get("text", "")

                source = (
                    chunk.get("source")
                    or chunk.get("document")
                    or "Unknown"
                )

                page = chunk.get("page")

            else:

                text = getattr(
                    chunk,
                    "text",
                    ""
                )

                source = getattr(
                    chunk,
                    "source",
                    "Unknown"
                )

                page = getattr(
                    chunk,
                    "page",
                    None
                )

            print(f"Source: {source}")

            if page is not None:
                print(f"Page: {page}")

            print(f"\n{text[:700]}")

            print("-" * 60)


if __name__ == "__main__":
    main()
