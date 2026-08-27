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


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT and DOCX files are supported."
        )

    safe_name = Path(file.filename).name
    document_id = uuid4().hex[:12]
    output_name = f"{document_id}_{safe_name}"
    output_path = DOCUMENTS_DIR / output_name

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        output_path.write_bytes(content)

        # ---------------------------------------------
        # READ DOCUMENT
        # ---------------------------------------------

        pages = load_file(output_path)

        chunks = []

        chunk_counter = 0

        for page_data in pages:

            page_chunks = chunk_text(
                page_data["text"]
            )

            for text in page_chunks:

                chunk_counter += 1

                chunks.append({
                    "chunk_id": (
                        f"{document_id}_"
                        f"{chunk_counter}"
                    ),
                    "text": text,
                    "document": output_name,
                    "page": page_data.get("page"),
                    "source": output_name,
                })

        if not chunks:
            output_path.unlink(missing_ok=True)

            raise HTTPException(
                status_code=400,
                detail="No readable text found in document."
            )

        # ---------------------------------------------
        # CREATE EMBEDDINGS
        # ---------------------------------------------

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = embedding_service.encode(
            texts
        )

        # ---------------------------------------------
        # ADD TO VECTOR STORE
        # ---------------------------------------------

        pipeline = get_pipeline()

        if pipeline is None:
            raise HTTPException(
                status_code=503,
                detail="RAG pipeline is not ready."
            )

        pipeline.vector_store.add(
            embeddings,
            chunks
        )

        # ---------------------------------------------
        # RESPONSE
        # ---------------------------------------------

        return {
            "success": True,
            "document_id": document_id,
            "filename": safe_name,
            "stored_as": output_name,
            "size_bytes": len(content),
            "chunks_created": len(chunks),
            "vectors_added": len(embeddings),
            "total_vectors": pipeline.vector_store.count(),
            "message": (
                "Document uploaded and indexed successfully."
            ),
        }

    except HTTPException:
        raise

    except Exception as error:

        if output_path.exists():
            output_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {error}"
        )
