from __future__ import annotations

from src.engines.base import BaseEngine
from src.engines.numbers import Numbers3Engine, Numbers4Engine
from src.engines.loto import Loto6Engine, Loto7Engine, MiniLotoEngine


def get_engine(game: str) -> BaseEngine:
    engines: dict[str, BaseEngine] = {
        "numbers3": Numbers3Engine(),
        "numbers4": Numbers4Engine(),
        "loto6": Loto6Engine(),
        "loto7": Loto7Engine(),
        "miniloto": MiniLotoEngine(),
    }
    try:
        return engines[game]
    except KeyError as exc:
        raise ValueError(f"未対応ゲームです: {game}") from exc
