import uuid
import threading
from datetime import datetime, timezone

_jobs = {}
_lock = threading.Lock()

def create_job(filename):
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    job = {
        "job_id": job_id,
        "filename": filename,
        "status": "queued",
        "stage": "Waiting to start",
        "progress": 0,
        "error": None,
        "created_at": now,
        "updated_at": now
    }

    with _lock:
        _jobs[job_id] = job

    return job

def update_job(job_id, status=None, stage=None, progress=None, error=None):
    with _lock:
        if job_id not in _jobs:
            return None

        if status is not None:
            _jobs[job_id]["status"] = status
        if stage is not None:
            _jobs[job_id]["stage"] = stage
        if progress is not None:
            _jobs[job_id]["progress"] = progress
        if error is not None:
            _jobs[job_id]["error"] = error

        _jobs[job_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

        return dict(_jobs[job_id])

def get_job(job_id):
    with _lock:
        job = _jobs.get(job_id)
        return dict(job) if job else None
