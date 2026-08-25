import os
from pathlib import Path

from dotenv import load_dotenv


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


# =========================================================
# ENVIRONMENT
# =========================================================

ENV_FILE = ROOT_DIR / ".env"

load_dotenv(ENV_FILE)


# =========================================================
# GEMINI
# =========================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)



# =========================================================
# EMBEDDING MODEL
# =========================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

EMBEDDING_DIMENSION = int(
    os.getenv(
        "EMBEDDING_DIMENSION",
        "384"
    )
)


# =========================================================
# RAG SETTINGS
# =========================================================

CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        "500"
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        "75"
    )
)

TOP_K = int(
    os.getenv(
        "TOP_K",
        "5"
    )
)

MIN_RELEVANCE_SCORE = float(
    os.getenv(
        "MIN_RELEVANCE_SCORE",
        "0.20"
    )
)


# =========================================================
# DIRECTORIES
# =========================================================

DOCUMENTS_DIR = ROOT_DIR / "documents"

KNOWLEDGE_BASE_DIR = (
    ROOT_DIR / "knowledge_base"
)

DATA_DIR = BASE_DIR / "data"


# =========================================================
# CREATE DIRECTORIES
# =========================================================

DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

KNOWLEDGE_BASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# FAISS FILES
# =========================================================

FAISS_INDEX_PATH = (
    DATA_DIR / "faiss.index"
)

CHUNKS_PATH = (
    DATA_DIR / "chunks.json"
)

METADATA_PATH = (
    DATA_DIR / "chunks_meta.json"
)


# =========================================================
# CONFIG VALIDATION
# =========================================================

def validate_config():

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Create a .env file in the project root "
            "and add your Gemini API key."
        )


    if EMBEDDING_DIMENSION <= 0:

        raise RuntimeError(
            "EMBEDDING_DIMENSION must be greater than 0."
        )


    if CHUNK_SIZE <= 0:

        raise RuntimeError(
            "CHUNK_SIZE must be greater than 0."
        )


    if CHUNK_OVERLAP < 0:

        raise RuntimeError(
            "CHUNK_OVERLAP cannot be negative."
        )


    if CHUNK_OVERLAP >= CHUNK_SIZE:

        raise RuntimeError(
            "CHUNK_OVERLAP must be smaller "
            "than CHUNK_SIZE."
        )# =========================================================
# CONFIDENCE / GROUNDING SETTINGS
# =========================================================

CONFIDENCE_HIGH = float(
    os.getenv(
        "CONFIDENCE_HIGH",
        "0.65"
    )
)

CONFIDENCE_MEDIUM = float(
    os.getenv(
        "CONFIDENCE_MEDIUM",
        "0.45"
    )
)

MIN_EVIDENCE_SCORE = float(
    os.getenv(
        "MIN_EVIDENCE_SCORE",
        "0.20"
    )
)
