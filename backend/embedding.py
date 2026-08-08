from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model ready")

    def encode(self, texts):

        return self.model.encode(
            texts,
            convert_to_numpy=True
        )


def create_embeddings(chunks):

    model = EmbeddingModel()

    embeddings = model.encode(
        chunks
    )

    return embeddings