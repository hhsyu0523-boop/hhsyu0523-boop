from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from database.update_service import DailyDatabaseUpdater


class SampleDataGenerator:
    """Creates starter CSV history files for all supported games."""

    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.updater = DailyDatabaseUpdater(self.data_dir)

    def generate(self) -> dict[str, Path]:
        games = ["numbers3", "numbers4", "miniloto", "loto6", "loto7"]
        created: dict[str, Path] = {}
        for game in games:
            digit_count = 3 if game in {"numbers3", "miniloto"} else 4 if game == "numbers4" else 6 if game == "loto6" else 7
            rows: list[dict[str, Any]] = []
            for idx in range(1, 9):
                values = [(idx + shift) % 10 for shift in range(digit_count)]
                rows.append({"draw_date": f"2026-01-{idx:02d}", "numbers": values, "game": game})
            created[game] = self.updater.update(game, rows)
        return created
