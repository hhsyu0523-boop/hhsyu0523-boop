from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd


class HistoricalDataset:
    """Loads and validates historical lottery data from CSV files."""

    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load(self, game: str) -> pd.DataFrame:
        path = self.data_dir / f"{game}.csv"
        if not path.exists():
            return pd.DataFrame(columns=["draw_date", "numbers", "game"])
        frame = pd.read_csv(path)
        frame["game"] = game
        return frame

    def validate(self, frame: pd.DataFrame) -> pd.DataFrame:
        if frame.empty:
            return frame
        required_columns = {"draw_date", "numbers", "game"}
        missing = required_columns.difference(frame.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        normalized = frame.copy()
        normalized["numbers"] = normalized["numbers"].apply(self._parse_numbers)
        normalized = normalized.dropna(subset=["numbers"])
        return normalized

    def save(self, game: str, frame: pd.DataFrame) -> Path:
        path = self.data_dir / f"{game}.csv"
        frame.to_csv(path, index=False)
        return path

    def _parse_numbers(self, value: Any) -> list[int] | None:
        print("value =", repr(value))
        if isinstance(value, str):
            value = value.replace("[", "").replace("]", "")
            tokens = [token.strip() for token in value.split(",") if token.strip()]
            if not tokens:
                return None
            try:
                return [int(token) for token in tokens]
            except ValueError:
                return None
        if isinstance(value, list):
            return [int(item) for item in value]
        return None
