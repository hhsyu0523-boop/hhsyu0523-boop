from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


class CSVStore:
    """Minimal CSV-based persistence helper for prediction data."""

    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, rows: list[dict[str, Any]]) -> Path:
        destination = self.data_dir / f"{name}.csv"
        frame = pd.DataFrame(rows)
        frame.to_csv(destination, index=False)
        return destination

    def load(self, name: str) -> pd.DataFrame:
        destination = self.data_dir / f"{name}.csv"
        if not destination.exists():
            return pd.DataFrame()
        return pd.read_csv(destination)
