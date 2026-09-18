from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from pathlib import Path
from datetime import datetime, timezone
import json
import uuid

router = APIRouter(prefix="/api/work", tags=["Work Management"])

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS_FILE = DATA_DIR / "projects.json"
TASKS_FILE = DATA_DIR / "tasks.json"


def load_json(path, default):
    if not path.exists():
        path.write_text(json.dumps(default, indent=2), encoding="utf-8")
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path, data):
    path.write_text(
        json.dumps(data, indent=2, default=str),
        encoding="utf-8"
    )


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str = ""
    department: str = "General"
    manager: str = "Project Manager"
    priority: str = "MEDIUM"
    status: str = "IN_PROGRESS"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    team_members: List[str] = []


class TaskCreate(BaseModel):
    project_id: str
    title: str = Field(..., min_length=2, max_length=200)
    description: str = ""
    assigned_to: str
    assigned_by: str = "Project Manager"
    priority: str = "MEDIUM"
    status: str = "TODO"
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    estimated_hours: float = 0
    dependencies: List[str] = []


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = Field(default=None, ge=0, le=100)
    due_date: Optional[str] = None
    actual_hours: Optional[float] = None


class StatusUpdate(BaseModel):
    status: str
    progress: int = Field(default=0, ge=0, le=100)


class CommentCreate(BaseModel):
    employee: str
    comment: str = Field(..., min_length=1, max_length=2000)


@router.get("/projects")
def get_projects():
    projects = load_json(PROJECTS_FILE, [])
    tasks = load_json(TASKS_FILE, [])

    for project in projects:
        project_tasks = [
            t for t in tasks if t.get("project_id") == project["id"]
        ]

        project["task_count"] = len(project_tasks)
        project["completed_tasks"] = len([
            t for t in project_tasks
            if t.get("status") == "COMPLETED"
        ])

        if project_tasks:
            project["progress"] = round(
                sum(t.get("progress", 0) for t in project_tasks)
                / len(project_tasks)
            )
        else:
            project["progress"] = 0

    return projects


@router.post("/projects")
def create_project(project: ProjectCreate):
    projects = load_json(PROJECTS_FILE, [])

    now = datetime.now(timezone.utc).isoformat()

    item = {
        "id": f"PRJ-{uuid.uuid4().hex[:8].upper()}",
        **project.model_dump(),
        "created_at": now,
        "updated_at": now
    }

    projects.append(item)
    save_json(PROJECTS_FILE, projects)

    return item


@router.get("/projects/{project_id}")
def get_project(project_id: str):
    projects = load_json(PROJECTS_FILE, [])
    tasks = load_json(TASKS_FILE, [])

    project = next(
        (p for p in projects if p["id"] == project_id),
        None
    )

    if not project:
        raise HTTPException(404, "Project not found")

    project["tasks"] = [
        t for t in tasks
        if t.get("project_id") == project_id
    ]

    return project


@router.get("/tasks")
def get_tasks(
    employee: Optional[str] = None,
    project_id: Optional[str] = None,
    status: Optional[str] = None
):
    tasks = load_json(TASKS_FILE, [])

    if employee:
        tasks = [
            t for t in tasks
            if t.get("assigned_to", "").lower()
            == employee.lower()
        ]

    if project_id:
        tasks = [
            t for t in tasks
            if t.get("project_id") == project_id
        ]

    if status:
        tasks = [
            t for t in tasks
            if t.get("status") == status
        ]

    return tasks


@router.post("/tasks")
def create_task(task: TaskCreate):
    projects = load_json(PROJECTS_FILE, [])
    tasks = load_json(TASKS_FILE, [])

    if not any(p["id"] == task.project_id for p in projects):
        raise HTTPException(404, "Project not found")

    now = datetime.now(timezone.utc).isoformat()

    item = {
        "id": f"TASK-{uuid.uuid4().hex[:8].upper()}",
        **task.model_dump(),
        "progress": 0,
        "actual_hours": 0,
        "comments": [],
        "created_at": now,
        "updated_at": now
    }

    tasks.append(item)
    save_json(TASKS_FILE, tasks)

    return item


@router.put("/tasks/{task_id}")
def update_task(task_id: str, update: TaskUpdate):
    tasks = load_json(TASKS_FILE, [])

    task = next(
        (t for t in tasks if t["id"] == task_id),
        None
    )

    if not task:
        raise HTTPException(404, "Task not found")

    changes = update.model_dump(exclude_none=True)
    task.update(changes)

    if task.get("status") == "COMPLETED":
        task["progress"] = 100

    task["updated_at"] = datetime.now(timezone.utc).isoformat()

    save_json(TASKS_FILE, tasks)

    return task


@router.post("/tasks/{task_id}/status")
def update_status(task_id: str, update: StatusUpdate):
    tasks = load_json(TASKS_FILE, [])

    task = next(
        (t for t in tasks if t["id"] == task_id),
        None
    )

    if not task:
        raise HTTPException(404, "Task not found")

    task["status"] = update.status
    task["progress"] = (
        100 if update.status == "COMPLETED"
        else update.progress
    )
    task["updated_at"] = datetime.now(timezone.utc).isoformat()

    save_json(TASKS_FILE, tasks)

    return task


@router.post("/tasks/{task_id}/comment")
def add_comment(task_id: str, comment: CommentCreate):
    tasks = load_json(TASKS_FILE, [])

    task = next(
        (t for t in tasks if t["id"] == task_id),
        None
    )

    if not task:
        raise HTTPException(404, "Task not found")

    task.setdefault("comments", []).append({
        "id": uuid.uuid4().hex[:10],
        "employee": comment.employee,
        "comment": comment.comment,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    task["updated_at"] = datetime.now(timezone.utc).isoformat()

    save_json(TASKS_FILE, tasks)

    return task


@router.get("/employee/{employee}")
def employee_work(employee: str):
    tasks = load_json(TASKS_FILE, [])
    projects = load_json(PROJECTS_FILE, [])

    employee_tasks = [
        t for t in tasks
        if t.get("assigned_to", "").lower()
        == employee.lower()
    ]

    completed = [
        t for t in employee_tasks
        if t.get("status") == "COMPLETED"
    ]

    active = [
        t for t in employee_tasks
        if t.get("status") != "COMPLETED"
    ]

    overdue = []

    today = datetime.now(timezone.utc).date().isoformat()

    for task in active:
        due = task.get("due_date")

        if due and due < today:
            overdue.append(task)

    project_ids = set(
        t.get("project_id")
        for t in employee_tasks
    )

    employee_projects = [
        p for p in projects
        if p.get("id") in project_ids
    ]

    attention = []

    for task in overdue:
        attention.append({
            "type": "OVERDUE",
            "title": task["title"],
            "task_id": task["id"]
        })

    for task in active:
        if task.get("priority") == "HIGH":
            attention.append({
                "type": "HIGH_PRIORITY",
                "title": task["title"],
                "task_id": task["id"]
            })

    return {
        "employee": employee,
        "summary": {
            "total_tasks": len(employee_tasks),
            "active_tasks": len(active),
            "completed_tasks": len(completed),
            "overdue_tasks": len(overdue)
        },
        "attention": attention,
        "tasks": employee_tasks,
        "projects": employee_projects
    }
