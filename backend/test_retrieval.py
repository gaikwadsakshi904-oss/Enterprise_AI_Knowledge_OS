from embedding import EmbeddingService
from vector_store import VectorStore


def main():

    print("=" * 60)
    print("FAISS RETRIEVAL TEST")
    print("=" * 60)

    # ------------------------------------------
    # Load services
    # ------------------------------------------

    embedding_service = (
        EmbeddingService()
    )

    store = VectorStore()

    print(
        f"\nIndexed vectors: "
        f"{store.count()}"
    )

    if store.count() == 0:

        print(
            "ERROR: FAISS index is empty."
        )

        return

    # ------------------------------------------
    # Query
    # ------------------------------------------

    question = input(
        "\nEnter your question: "
    ).strip()

    if not question:

        print(
            "Question cannot be empty."
        )

        return

    # ------------------------------------------
    # Create query embedding
    # ------------------------------------------

    query_embedding = (
        embedding_service.encode(
            [question]
        )
    )

    # ------------------------------------------
    # Search
    # ------------------------------------------

    results = store.search(
        query_embedding,
        top_k=5,
    )

    # ------------------------------------------
    # Display
    # ------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "SEARCH RESULTS"
    )

    print(
        "=" * 60
    )

    for position, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n#{position}"
        )

        print(
            f"Document: "
            f"{result['document']}"
        )

        print(
            f"Page: "
            f"{result['page']}"
        )

        print(
            f"Score: "
            f"{result['score']}"
        )

        print(
            f"Chunk ID: "
            f"{result['chunk_id']}"
        )

        print(
            "\nText:"
        )

        print(
            result["text"][:500]
        )

        print(
            "-" * 60
        )


if __name__ == "__main__":

    main()