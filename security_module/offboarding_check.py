import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "offboarding.sqlite3"


def get_employee_status(employee_id: str) -> str:
    """Return active, terminated, or not_registered."""
    if not employee_id or not employee_id.strip():
        return "not_registered"

    if not DB_PATH.exists():
        return "not_registered"

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT status FROM employee_status WHERE employee_id = ?",
            (employee_id.strip(),),
        ).fetchone()

    return row[0] if row else "not_registered"
