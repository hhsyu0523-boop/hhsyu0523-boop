from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class EvaluationReporter:
    """Writes evaluation summaries to CSV for each run."""

    def save(self, rows: list[dict[str, Any]], output_path: str | Path) -> Path:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["game", "metric", "value"])
            writer.writeheader()
            writer.writerows(rows)
        return destination
