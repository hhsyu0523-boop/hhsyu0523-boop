from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PredictionResult:
    engine_name: str
    mode: str
    predictions: list[int]
    metadata: dict[str, Any] = field(default_factory=dict)


class BasePredictionEngine:
    """Base class for all lottery prediction engines."""

    def __init__(self, engine_name: str) -> None:
        self.engine_name = engine_name

    def predict(self, history: list[dict[str, Any]] | None = None) -> PredictionResult:
        raise NotImplementedError
