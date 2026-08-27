from fastapi import APIRouter, HTTPException
from job_manager import get_job

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("/{job_id}")
def job_status(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
