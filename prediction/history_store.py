from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class PredictionHistoryStore:
    """Saves prediction history to CSV for audit and reporting."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, rows: list[dict[str, Any]], filename: str = "prediction_history.csv") -> Path:
        path = self.output_dir / filename
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["game", "engine", "prediction", "score", "timestamp"])
            writer.writeheader()
            writer.writerows(rows)
        return path
