import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/security/offboarding",
    tags=["Employee Security"]
)

DB_PATH = Path(__file__).resolve().parent / "offboarding.sqlite3"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def now():
    return datetime.now(timezone.utc).isoformat()


def initialize_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employee_status (
                employee_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT NOT NULL,
                action TEXT NOT NULL,
                performed_by TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                reason TEXT
            )
        """)


class OffboardRequest(BaseModel):
    employee_id: str = Field(min_length=1, max_length=100)
    reason: str = Field(
        default="Employment ended",
        max_length=500
    )


def verify_admin(key: str):
    expected = os.environ.get("OFFBOARDING_ADMIN_KEY")
    if not expected or key != expected:
        raise HTTPException(
            status_code=403,
            detail="Admin authorization failed"
        )


@router.post("/deactivate")
def deactivate_employee(
    request: OffboardRequest,
    x_admin_key: str = Header()
):
    verify_admin(x_admin_key)
    employee_id = request.employee_id.strip()

    if not employee_id:
        raise HTTPException(400, "Invalid employee ID")

    timestamp = now()

    with get_db() as conn:
        conn.execute("""
            INSERT INTO employee_status
                (employee_id, status, updated_at)
            VALUES (?, 'terminated', ?)
            ON CONFLICT(employee_id) DO UPDATE SET
                status = 'terminated',
                updated_at = excluded.updated_at
        """, (employee_id, timestamp))

        conn.execute("""
            INSERT INTO audit_log
                (employee_id, action, performed_by, timestamp, reason)
            VALUES (?, ?, ?, ?, ?)
        """, (
            employee_id,
            "employee_deactivated",
            "authorized_admin",
            timestamp,
            request.reason
        ))

    return {
        "success": True,
        "employee_id": employee_id,
        "status": "terminated",
        "message": (
            "Status recorded. Existing application access "
            "is not automatically revoked by this standalone module."
        )
    }


@router.get("/status/{employee_id}")
def get_employee_status(employee_id: str):
    with get_db() as conn:
        row = conn.execute("""
            SELECT employee_id, status, updated_at
            FROM employee_status
            WHERE employee_id = ?
        """, (employee_id,)).fetchone()

    if row is None:
        return {
            "employee_id": employee_id,
            "status": "not_registered"
        }

    return dict(row)


@router.get("/audit")
def get_audit_log(x_admin_key: str = Header()):
    verify_admin(x_admin_key)

    with get_db() as conn:
        rows = conn.execute("""
            SELECT employee_id, action, performed_by, timestamp, reason
            FROM audit_log
            ORDER BY id DESC
            LIMIT 500
        """).fetchall()

    return {"audit_log": [dict(row) for row in rows]}


initialize_db()


# ------------------------------------------------------------
# Employee email mapping and authorized email status lookup
# ------------------------------------------------------------

class EmployeeEmailRequest(BaseModel):
    employee_id: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=254)


with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employee_email (
            email TEXT PRIMARY KEY COLLATE NOCASE,
            employee_id TEXT NOT NULL
        )
    """)


@router.post("/register-email")
def register_employee_email(
    request: EmployeeEmailRequest,
    x_admin_key: str = Header()
):
    verify_admin(x_admin_key)

    employee_id = request.employee_id.strip()
    email = request.email.strip().lower()

    if not employee_id or "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Invalid employee ID or email")

    with get_db() as conn:
        conn.execute("""
            INSERT INTO employee_email (email, employee_id)
            VALUES (?, ?)
            ON CONFLICT(email) DO UPDATE SET
                employee_id = excluded.employee_id
        """, (email, employee_id))

    return {
        "success": True,
        "employee_id": employee_id,
        "email": email,
        "message": "Email mapping registered"
    }


@router.get("/status-by-email")
def get_employee_status_by_email(
    email: str,
    x_admin_key: str = Header()
):
    verify_admin(x_admin_key)

    with get_db() as conn:
        mapping = conn.execute("""
            SELECT employee_id FROM employee_email
            WHERE email = ? COLLATE NOCASE
        """, (email.strip(),)).fetchone()

        if mapping is None:
            return {"email": email, "status": "not_registered"}

        employee_id = mapping["employee_id"]
        row = conn.execute("""
            SELECT employee_id, status, updated_at
            FROM employee_status
            WHERE employee_id = ?
        """, (employee_id,)).fetchone()

    if row is None:
        return {
            "email": email,
            "employee_id": employee_id,
            "status": "active"
        }

    return {**dict(row), "email": email}
