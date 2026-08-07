from embedding import EmbeddingModel
from vector_store import VectorStore

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

store.add(
    embeddings,
    texts
)

query = model.encode(
    ["AI"]
)[0]

results = store.search(
    query,
    k=3
)

print("\nMost Similar Documents\n")

for item in results:
    print(item)