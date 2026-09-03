import json
import os
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/employee", tags=["Employee Intelligence"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ACTIVITY_FILE = os.path.join(DATA_DIR, "employee_activity.json")

_lock = Lock()


class ActivityRequest(BaseModel):
    employee: str = Field(default="Current Employee", max_length=150)
    activity_type: str = Field(..., max_length=100)
    title: str = Field(..., max_length=300)
    description: str = Field(default="", max_length=1000)
    metadata: Dict[str, Any] = Field(default_factory=dict)


def _ensure_file():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(ACTIVITY_FILE):
        with open(ACTIVITY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def _read():
    _ensure_file()

    try:
        with open(ACTIVITY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, list) else []

    except Exception:
        return []


def _write(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(ACTIVITY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@router.post("/activity")
def record_activity(request: ActivityRequest):

    employee = request.employee.strip() or "Current Employee"

    activity = {
        "id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f"),
        "employee": employee,
        "activity_type": request.activity_type,
        "title": request.title,
        "description": request.description,
        "metadata": request.metadata,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    with _lock:
        activities = _read()
        activities.insert(0, activity)
        activities = activities[:500]
        _write(activities)

    return {
        "status": "recorded",
        "activity": activity,
    }


@router.get("/workspace")
def get_employee_workspace(employee: str = "Current Employee"):

    employee = employee.strip() or "Current Employee"

    with _lock:
        activities = _read()

    employee_activities = [
        item
        for item in activities
        if item.get("employee") == employee
    ]

    employee_activities = employee_activities[:30]

    # --------------------------------------------------------
    # Recent company activity
    # --------------------------------------------------------

    company_activity = activities[:20]

    # --------------------------------------------------------
    # My work
    # --------------------------------------------------------

    investigations = [
        item
        for item in employee_activities
        if item.get("activity_type") == "investigation_completed"
    ]

    uploads = [
        item
        for item in employee_activities
        if item.get("activity_type") == "document_uploaded"
    ]

    # --------------------------------------------------------
    # Attention items
    # --------------------------------------------------------

    attention = []

    if len(investigations) == 0:
        attention.append({
            "id": "start-investigation",
            "priority": "medium",
            "title": "Start your first AI investigation",
            "description": "Ask the AI about company policies, documents or business questions.",
            "action": "Open Investigation",
        })

    if len(uploads) > 0:
        latest_upload = uploads[0]

        attention.append({
            "id": "review-document",
            "priority": "low",
            "title": "Review your latest uploaded document",
            "description": latest_upload.get("title", "Document uploaded"),
            "action": "Open Knowledge Base",
        })

    return {
        "employee": employee,
        "generated_at": datetime.now(timezone.utc).isoformat(),

        "attention": attention,

        "my_work": {
            "investigations": len(investigations),
            "documents_uploaded": len(uploads),
            "activities": len(employee_activities),
        },

        "company_activity": company_activity,

        "my_activity": employee_activities,
    }
