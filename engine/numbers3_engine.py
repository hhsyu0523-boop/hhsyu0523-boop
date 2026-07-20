from __future__ import annotations

from typing import Any

from engine.base import BasePredictionEngine, PredictionResult
from prediction.box_priority import BoxPriorityEngine


class Numbers3PredictionEngine(BasePredictionEngine):
    """BOX priority prediction engine for Numbers3."""

    def __init__(self) -> None:
        super().__init__(engine_name="numbers3")
        self.box_engine = BoxPriorityEngine()

    def predict(self, history: list[dict[str, Any]] | None = None) -> PredictionResult:
        ranked = self.box_engine.generate(history=history, digits=3, limit=10)
        return PredictionResult(
            engine_name=self.engine_name,
            mode="box_priority",
            predictions=[item["combination"] for item in ranked],
            metadata={
                "strategy": "frequency_bias",
                "history_size": len(history or []),
                "ranking": ranked,
            },
        )
