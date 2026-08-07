from embedding import EmbeddingModel

model = EmbeddingModel()

texts = [
    "Artificial Intelligence",
    "Machine Learning"
]

embeddings = model.encode(texts)

print("Embedding Shape:", embeddings.shape)
print("First Vector Length:", len(embeddings[0]))