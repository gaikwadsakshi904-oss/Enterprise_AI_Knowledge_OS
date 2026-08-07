from embedding import EmbeddingModel
from vector_store import VectorStore


class DocumentSimilarity:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore(384)

    def load_store(self, index_path, chunk_path):

        self.vector_store.load(index_path, chunk_path)

    def search(self, query, k=3):

        query_embedding = self.embedding_model.encode([query])[0]

        results = self.vector_store.search(query_embedding, k)

        return results