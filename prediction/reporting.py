from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class PredictionReportExporter:
    """Exports ranked prediction results to CSV."""

    def export(self, rows: list[dict[str, Any]], output_path: str | Path) -> Path:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["engine", "rank_type", "digits", "combination", "score"])
            writer.writeheader()
            for row in rows:
                writer.writerow(
                    {
                        "engine": row.get("engine", "unknown"),
                        "rank_type": row.get("rank_type", "box"),
                        "digits": row.get("digits", 3),
                        "combination": "-".join(str(value) for value in row.get("combination", [])),
                        "score": row.get("score", 0),
                    }
                )
        return destination
