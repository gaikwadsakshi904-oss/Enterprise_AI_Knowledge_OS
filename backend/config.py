import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DOCUMENT_FOLDER = os.path.join(PROJECT_DIR, "documents")

DATASET_FOLDER = os.path.join(BASE_DIR, "datasets")
EMBEDDING_FOLDER = os.path.join(BASE_DIR, "embeddings")
MODEL_FOLDER = os.path.join(BASE_DIR, "models")
METADATA_FOLDER = os.path.join(BASE_DIR, "metadata")

FAISS_INDEX = os.path.join(MODEL_FOLDER, "faiss_index.bin")
CHUNKS_FILE = os.path.join(MODEL_FOLDER, "chunks.json")