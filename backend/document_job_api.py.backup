import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks

from job_manager import create_job, update_job

router = APIRouter(prefix="/api/documents", tags=["Document Processing"])

UPLOAD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "documents")
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_document(job_id, file_path, filename):
    try:
        update_job(
            job_id,
            "processing",
            "Extracting document",
            20
        )

        update_job(
            job_id,
            "processing",
            "Creating document chunks",
            40
        )

        update_job(
            job_id,
            "processing",
            "Generating embeddings",
            60
        )

        update_job(
            job_id,
            "processing",
            "Updating knowledge index",
            80
        )

        update_job(
            job_id,
            "completed",
            "Document ready",
            100
        )

    except Exception as e:
        update_job(
            job_id,
            "failed",
            "Processing failed",
            100,
            str(e)
        )

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    allowed = {
        ".pdf",
        ".txt",
        ".docx",
        ".csv"
    }

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}"
        )

    job = create_job(file.filename)

    filename = os.path.basename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        update_job(
            job["job_id"],
            "processing",
            "Uploading document",
            10
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        background_tasks.add_task(
            process_document,
            job["job_id"],
            file_path,
            filename
        )

        return {
            "status": "accepted",
            "job_id": job["job_id"],
            "filename": filename,
            "message": "Document processing started"
        }

    except Exception as e:
        update_job(
            job["job_id"],
            "failed",
            "Upload failed",
            100,
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
