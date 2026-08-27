import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class InvestigationMemory:

    def __init__(self, file_path="data/investigation_history.json"):

        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file_path.exists():

            self.file_path.write_text(
                "[]",
                encoding="utf-8"
            )

    def save(self, investigation: Dict):

        history = self.load()

        record = {
            "id": len(history) + 1,
            "timestamp": datetime.now().isoformat(),
            "objective": investigation.get(
                "objective",
                ""
            ),
            "status": investigation.get(
                "status",
                "unknown"
            ),
            "evidence_count": len(
                investigation.get(
                    "findings",
                    []
                )
            ),
            "source_count": len(
                investigation.get(
                    "sources",
                    []
                )
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

    def load(self) -> List[Dict]:

        try:

            return json.loads(
                self.file_path.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return []

    def latest(self, limit=10):

        history = self.load()

        return history[-limit:]

    def clear(self):

        self.file_path.write_text(
            "[]",
            encoding="utf-8"
        )
