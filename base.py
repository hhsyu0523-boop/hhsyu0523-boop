from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseEngine(ABC):
    game_key: str
    display_name: str

    def default_data_path(self) -> Path:
        return Path("data") / self.game_key

    @abstractmethod
    def predict(self, data_path: Path, count: int) -> list[str]:
        raise NotImplementedError
