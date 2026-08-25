from document_loader import load_documents
from embedding import EmbeddingService
from vector_store import VectorStore


def main():

    print("=" * 60)
    print("ENTERPRISE AI KNOWLEDGE OS")
    print("Building Knowledge Index")
    print("=" * 60)

    # ----------------------------------------
    # 1. Load documents
    # ----------------------------------------

    print("\n[1/3] Loading documents...")

    chunks = load_documents()

    if not chunks:
        print(
            "No documents found."
        )
        return

    print(
        f"Loaded {len(chunks)} chunks."
    )

    # ----------------------------------------
    # 2. Create embeddings
    # ----------------------------------------

    print(
        "\n[2/3] Creating embeddings..."
    )

    embedding_service = EmbeddingService()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_service.encode(
        texts
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    # ----------------------------------------
    # 3. Build FAISS index
    # ----------------------------------------

    print(
        "\n[3/3] Building FAISS index..."
    )

    store = VectorStore()

    store.build(
        embeddings,
        chunks
    )

    print("\n" + "=" * 60)
    print("INDEX BUILD COMPLETE")
    print("=" * 60)

    print(
        f"Chunks indexed: {store.count()}"
    )


if __name__ == "__main__":
    main()