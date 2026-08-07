from embedding import EmbeddingModel
from vector_store import VectorStore
from config import FAISS_INDEX, CHUNKS_FILE


# Sample documents

documents = [
    """
    Artificial Intelligence is a branch of computer science
    that enables machines to perform tasks requiring human
    intelligence.
    """,

    """
    Machine Learning is a subset of Artificial Intelligence
    where machines learn patterns from data.
    """,

    """
    Deep Learning is a subset of Machine Learning that uses
    artificial neural networks with multiple layers.
    It is used in image recognition, speech recognition,
    natural language processing and autonomous vehicles.
    """
]


# Load embedding model

embedding_model = EmbeddingModel()


# Create embeddings

vectors = embedding_model.encode(
    documents
)


# Create vector store

vector_store = VectorStore(384)


vector_store.create(
    vectors,
    documents
)


vector_store.save(
    FAISS_INDEX,
    CHUNKS_FILE
)


print("Embeddings created successfully!")