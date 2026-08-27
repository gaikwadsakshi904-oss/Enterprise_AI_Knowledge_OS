from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from config import DOCUMENTS_DIR
from document_loader import load_file, chunk_text
from embedding import EmbeddingService


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".docx",
}


embedding_service = EmbeddingService()


def get_pipeline():
    from app import pipeline
    return pipeline




