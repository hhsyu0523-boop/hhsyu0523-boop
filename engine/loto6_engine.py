from __future__ import annotations

from typing import Any

from engine.base import BasePredictionEngine, PredictionResult
from prediction.box_priority import BoxPriorityEngine


class Loto6PredictionEngine(BasePredictionEngine):
    """BOX ranking engine for Loto6."""

    def __init__(self) -> None:
        super().__init__(engine_name="loto6")
        self.box_engine = BoxPriorityEngine()

    def predict(self, history: list[dict[str, Any]] | None = None) -> PredictionResult:
        ranked = self.box_engine.generate(history=history, digits=6, limit=10)
        return PredictionResult(
            engine_name=self.engine_name,
            mode="feature_engineering",
            predictions=[item["combination"] for item in ranked],
            metadata={
                "strategy": "feature_engineering",
                "history_size": len(history or []),
                "ranking": ranked,
            },
        )
