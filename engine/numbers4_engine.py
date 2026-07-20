from __future__ import annotations

from collections import Counter
from typing import Any

from engine.base import BasePredictionEngine, PredictionResult
from prediction.box_priority import BoxPriorityEngine


class Numbers4PredictionEngine(BasePredictionEngine):
    """Numbers4 BOX-first prediction engine."""

    def __init__(self) -> None:
        super().__init__(engine_name="numbers4")
        self.box_engine = BoxPriorityEngine()

    def predict(
        self,
        history: list[dict[str, Any]] | None = None,
    ) -> PredictionResult:
        history = history or []

        # 候補を十分に作成
        ranked = self.box_engine.generate(
            history=history,
            digits=4,
            limit=120,
        )

        singles: list[dict[str, Any]] = []
        doubles: list[dict[str, Any]] = []

        for item in ranked:
            combination = item["combination"]
            counts = Counter(combination)
            repeated_digits = sum(
                count - 1
                for count in counts.values()
                if count > 1
            )

            if repeated_digits == 0:
                singles.append(item)
            elif repeated_digits == 1:
                doubles.append(item)

        # BOX優先12口＋ダブル3口
        selected = singles[:12] + doubles[:3]

        # 不足時だけ残り候補から補充
        selected_keys = {
            tuple(item["combination"])
            for item in selected
        }

        if len(selected) < 15:
            for item in ranked:
                key = tuple(item["combination"])

                if key in selected_keys:
                    continue

                selected.append(item)
                selected_keys.add(key)

                if len(selected) >= 15:
                    break

        # 表示順は12口の通常候補、その後にダブル3口
        for index, item in enumerate(selected):
            item["ticket_type"] = (
                "double"
                if index >= 12
                else "box"
            )

        return PredictionResult(
            engine_name=self.engine_name,
            mode="box_priority_12_plus_double_3",
            predictions=[
                item["combination"]
                for item in selected
            ],
            metadata={
                "strategy": "box_priority_12_plus_double_3",
                "history_size": len(history),
                "single_count": min(12, len(singles)),
                "double_count": min(3, len(doubles)),
                "ranking": selected,
            },
        )