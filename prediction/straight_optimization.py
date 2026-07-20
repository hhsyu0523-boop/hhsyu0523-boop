from __future__ import annotations

from collections import Counter
from typing import Any


class StraightOptimizationEngine:
    """
    Straight ranking engine.
    Uses recent draw frequency to rank straight candidates.
    """

    def generate(
        self,
        history: list[dict[str, Any]] | None = None,
        digits: int = 4,
        limit: int = 15,
    ) -> list[dict[str, Any]]:

        if history is None:
            history = []

        counter = Counter()

        for draw in history:
            numbers = draw.get("numbers", [])

            if isinstance(numbers, str):
                numbers = [int(x) for x in numbers.split(",") if x.strip()]

            if isinstance(numbers, list):
                for n in numbers:
                    counter[int(n)] += 1

        ranking = []

        for number, score in counter.most_common(limit):
            ranking.append(
                {
                    "combination": [number],
                    "score": float(score),
                    "rank_type": "straight",
                }
            )

        return ranking