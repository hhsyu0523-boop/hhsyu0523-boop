from __future__ import annotations

from pathlib import Path


import pandas as pd

from database.dataset import HistoricalDataset


class DataLoader:
    """Shared loader for all historical lottery datasets."""

    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.dataset = HistoricalDataset(self.data_dir)

    def load_game(self, game: str) -> pd.DataFrame:
        frame = self.dataset.load(game)
        if frame.empty:
            return pd.DataFrame(columns=["draw_date", "numbers", "game"])
        return self.dataset.validate(frame)

    def load_all(self) -> dict[str, pd.DataFrame]:
        games = ["numbers3", "numbers4", "miniloto", "loto6", "loto7"]
        return {game: self.load_game(game) for game in games}
