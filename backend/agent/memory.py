import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


class InvestigationMemory:

    def __init__(self, file_path="data/investigation_history.json"):
        self.file_path = Path(file_path)

        if not self.file_path.is_absolute():
            self.file_path = Path(__file__).resolve().parent.parent / self.file_path

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file_path.exists():
            self.file_path.write_text(
                "[]",
                encoding="utf-8"
            )

    def load(self) -> List[Dict]:
        try:
            return json.loads(
                self.file_path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return []

    def save(self, investigation: Dict):

        history = self.load()

        now = datetime.now(timezone.utc)

        start_time = investigation.get(
            "started_at"
        )

        completed_time = investigation.get(
            "completed_at"
        )

        if not start_time:
            start_time = now.isoformat()

        if not completed_time:
            completed_time = now.isoformat()

        duration_seconds = investigation.get(
            "duration_seconds"
        )

        if duration_seconds is None:
            try:
                start_dt = datetime.fromisoformat(
                    start_time.replace("Z", "+00:00")
                )

                end_dt = datetime.fromisoformat(
                    completed_time.replace("Z", "+00:00")
                )

                duration_seconds = round(
                    (end_dt - start_dt).total_seconds(),
                    2
                )

            except Exception:
                duration_seconds = 0

        record = {
            "id": len(history) + 1,

            "investigation_id": investigation.get(
                "investigation_id",
                f"INV-{now.strftime('%Y%m%d-%H%M%S')}-{len(history)+1:04d}"
            ),

            "employee": investigation.get(
                "employee",
                investigation.get(
                    "user",
                    "System User"
                )
            ),

            "timestamp": now.isoformat(),

            "started_at": start_time,

            "completed_at": completed_time,

            "duration_seconds": duration_seconds,

            "objective": investigation.get(
                "objective",
                ""
            ),

            "status": investigation.get(
                "status",
                "completed"
            ),

            "evidence_count": investigation.get(
                "evidence_count",
                0
            ),

            "source_count": investigation.get(
                "source_count",
                0
            ),

            "work_completed": investigation.get(
                "work_completed",
                [
                    "Knowledge retrieval",
                    "Hybrid search",
                    "Evidence reranking",
                    "AI analysis",
                    "Confidence evaluation",
                    "Executive report generation"
                ]
            ),

            "report": investigation.get(
                "report",
                ""
            ),
        }

        history.append(record)

        self.file_path.write_text(
            json.dumps(
                history,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return record

    def latest(self, limit=10):

        history = self.load()

        return history[-limit:]

    def clear(self):

        self.file_path.write_text(
            "[]",
            encoding="utf-8"
        )
