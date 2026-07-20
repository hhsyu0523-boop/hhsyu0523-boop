from __future__ import annotations

from collections import Counter
from itertools import combinations,combinations_with_replacement
from string import digits
from typing import Any
from weights import DEFAULT_WEIGHTS
class BoxPriorityEngine:
    """Production-quality BOX priority ranking helper for lottery games."""

    def generate(
        self,
        history: list[dict[str, Any]] | None = None,
        digits: int = 3,
        limit: int = 10,
        min_value: int = 0,
        max_value: int = 9,
    ) -> list[dict[str, Any]]:
        if history is None:
            history = []

        normalized_history: list[list[int]] = []
        for item in history:
            normalized = self._normalize_draw(item)
            if normalized is not None:
                normalized_history.append(normalized)

        if not normalized_history:
            return []

        pool = list(range(min_value, max_value + 1))
        number_scores = Counter()
        for idx, draw in enumerate(reversed(normalized_history)):
            recency = idx + 1
            for value in draw:
                number_scores[value] += 1.2 / recency

        for draw in normalized_history:
            for position, value in enumerate(draw):
                number_scores[value] += 0.6 / (position + 1)

        scored: list[dict[str, Any]] = []
        if digits == 4:
            # シングル候補
            single_iter = combinations(pool, digits)

            # ダブル候補（2個同じ数字）
            double_iter = (
                combo
                for combo in combinations_with_replacement(pool, digits)
                if len(set(combo)) == 3
            )

            import itertools
            candidate_iter = itertools.chain(single_iter, double_iter)

        else:
            candidate_iter = combinations(pool, digits)

        for combo in candidate_iter:
            score = self._score_combination(
                combo,
                normalized_history,
                digits,
            )

            if score > 0:
                scored.append(
                    {
                        "combination": list(combo),
                        "score": round(score + sum(number_scores.get(value, 0) for value in combo) * 0.2, 4),
                        "rank_type": "box",
                        "digits": digits,
                    }
                )

        scored.sort(key=lambda item: item["score"], reverse=True)
        return self._diversity_filter(scored, limit)

    def generate_straight_rankings(
        self,
        history: list[dict[str, Any]] | None = None,
        digits: int = 3,
        limit: int = 10,
        min_value: int = 0,
        max_value: int = 9,
    ) -> list[dict[str, Any]]:
        ranked = self.generate(history=history, digits=digits, limit=limit, min_value=min_value, max_value=max_value)
        return [
            {
                **item,
                "rank_type": "straight",
                "score": round(item["score"] * 1.15, 4),
            }
            for item in ranked
        ]

    def export_report(
        self,
        history: list[dict[str, Any]] | None = None,
        digits: int = 3,
        limit: int = 10,
        min_value: int = 0,
        max_value: int = 9,
        output_path: str | None = None,
    ) -> list[dict[str, Any]]:
        ranked = self.generate(history=history, digits=digits, limit=limit, min_value=min_value, max_value=max_value)
        straight = self.generate_straight_rankings(history=history, digits=digits, limit=limit, min_value=min_value, max_value=max_value)
        rows = ranked + straight
        if output_path:
            import csv

            with open(output_path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["rank_type", "digits", "combination", "score"])
                writer.writeheader()
                for row in rows:
                    writer.writerow({
                        "rank_type": row["rank_type"],
                        "digits": row["digits"],
                        "combination": "-".join(str(value) for value in row["combination"]),
                        "score": row["score"],
                    })
        return rows

    def _normalize_draw(self, item: dict[str, Any]) -> list[int] | None:
        numbers = item.get("numbers")
        if isinstance(numbers, list):
            normalized = [int(value) for value in numbers if str(value).isdigit()]
            if normalized:
                return normalized
        if isinstance(numbers, str):
            tokens = [token.strip() for token in numbers.split(",") if token.strip()]
            try:
                return [int(token) for token in tokens]
            except ValueError:
                return None
        return None

    def _score_combination(
        self,
        combo: tuple[int, ...],
        history: list[list[int]],
        digits: int,
    ) -> float:
        frequency_score = self._frequency_score(combo, history)
        delay_score = self._delay_score(combo, history)
        hot_cold_score = self._hot_cold_score(combo, history)
        positional_score = self._positional_score(combo, history)
        transition_score = self._transition_score(combo, history)
        pair_score = self._pair_score(combo, history)
        double_score = self._double_score(combo, history)
        repeat_score = self._repeat_score(combo, history)
        mirror_score = self._mirror_score(combo, history)

        total_score = (
            frequency_score
            + delay_score
            + hot_cold_score
            + positional_score
            + transition_score
            + pair_score
            + (double_score * 2.2)
            + repeat_score
            + mirror_score
        )
        return total_score / max(1, digits)

    def _frequency_score(
        self,
        combo: tuple[int, ...],
        history: list[list[int]],
    ) -> float:
        counts = Counter(
            value
            for draw in history
            for value in draw
        )

        return (
            sum(counts.get(value, 0) for value in combo)
            * DEFAULT_WEIGHTS["frequency"]
        )
    def _delay_score(
        self,
        combo: tuple[int, ...],
        history: list[list[int]],
    ) -> float:
        score = 0.0

        for value in combo:
            last_seen = 0

            for idx, draw in enumerate(history):
                if value in draw:
                    last_seen = len(history) - idx
                    break

            score += max(0, 10 - last_seen)

        return score * 0.1

    def _hot_cold_score(self, combo: tuple[int, ...], history: list[list[int]]) -> float:
        counts = Counter(value for draw in history for value in draw)
        total = max(1, len(history) * len(history[0]) if history else 1)
        score = 0.0
        for value in combo:
            score += counts.get(value, 0) / total
        return score * 10

    def _positional_score(self, combo: tuple[int, ...], history: list[list[int]]) -> float:
        score = 0.0
        for position, value in enumerate(combo):
            position_counts = Counter(draw[position] for draw in history if len(draw) > position)
            score += position_counts.get(value, 0)
        return score * 0.15

    def _transition_score(self, combo: tuple[int, ...], history: list[list[int]]) -> float:
        if len(history) < 2:
            return 0.0
        score = 0.0
        for previous, current in zip(history[:-1], history[1:]):
            if set(combo).intersection(previous) and set(combo).intersection(current):
                score += 1
        return score * 0.8

    def _pair_score(self, combo: tuple[int, ...], history: list[list[int]]) -> float:
        score = 0.0
        for pair in combinations(combo, 2):
            pair_count = sum(1 for draw in history if pair[0] in draw and pair[1] in draw)
            score += pair_count
        return score * 0.2

    def _double_score(
        self,
        combo: tuple[int, ...],
        history: list[list[int]],
    ) -> float:

        combo_counter = Counter(combo)

        # ダブル・トリプル判定
        duplicate_count = sum(
            count - 1
            for count in combo_counter.values()
            if count > 1
        )

        if duplicate_count == 0:
            return 0.0

        score = duplicate_count * 1.2

        # 直近100回で同じ数字のダブル出現頻度を調査
        recent = history[-100:] if len(history) >= 100 else history

        for value, count in combo_counter.items():

            if count < 2:
                continue

            freq = 0

            for draw in recent:
                draw_counter = Counter(draw)
                if draw_counter[value] >= 2:
                    freq += 1

            # 少ないほど加点
            score += max(0.0, 1.5 - (freq * 0.08))

        return round(score, 4)

    def _repeat_score(self, combo: tuple[int, ...], history: list[list[int]]) -> float:
        score = 0.0
        for value in combo:
            if any(value in draw for draw in history):
                score += 1
        return score * 0.4

    def _mirror_score(self, combo: tuple[int, ...], history: list[list[int]]) -> float:
        score = 0.0
        for value in combo:
            mirror = 9 - value
            if any(mirror in draw for draw in history):
                score += 0.2
        return score
    def _diversity_filter(
        self,
        scored: list[dict[str, Any]],
        limit: int,
    ) -> list[dict[str, Any]]:
        """
        BOX候補の多様性を維持しながら、
        ダブル候補を必ず残すフィルター
        """

        selected: list[dict[str, Any]] = []
        double_selected = 0

        for candidate in scored:

            combo = candidate["combination"]
            combo_set = set(combo)

            # ダブル判定
            is_double = len(combo_set) < len(combo)

            duplicate = False

            # ダブルは最大3件まで優先採用
            if is_double:
                if double_selected < 3:
                    selected.append(candidate)
                    double_selected += 1
                continue

            # シングルのみ重複チェック
            for picked in selected:

                picked_combo = picked["combination"]

                # ダブル候補とは比較しない
                if len(set(picked_combo)) < len(picked_combo):
                    continue

                overlap = len(combo_set & set(picked_combo))

                if len(combo) == 4:
                    if overlap >= 3:
                        duplicate = True
                        break
                else:
                    if overlap >= 2:
                        duplicate = True
                        break

            if not duplicate:
                selected.append(candidate)

            if len(selected) >= limit:
                break

        return selected[:limit]