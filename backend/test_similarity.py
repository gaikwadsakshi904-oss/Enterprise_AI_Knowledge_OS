from embedding import EmbeddingModel
from vector_store import VectorStore
from document_similarity import DocumentSimilarity

texts = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Python Programming",
    "FastAPI Backend"
]

model = EmbeddingModel()

embeddings = model.encode(texts)

store = VectorStore(384)

store.add(embeddings, texts)

store.save(
    "models/faiss_index.bin",
    "models/chunks.json"
)

similarity = DocumentSimilarity()

similarity.load_store(
    "models/faiss_index.bin",
    "models/chunks.json"
)

results = similarity.search("AI")

print(results)