from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from database.dataset import HistoricalDataset


class DailyDatabaseUpdater:
    """Maintains a local CSV database with daily snapshots of historical data."""

    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.dataset = HistoricalDataset(self.data_dir)

    def update(self, game: str, rows: list[dict[str, Any]]) -> Path:
        frame = pd.DataFrame(rows)
        if frame.empty:
            frame = pd.DataFrame(columns=["draw_date", "numbers", "game"])
        validated = self.dataset.validate(frame)
        return self.dataset.save(game, validated)
