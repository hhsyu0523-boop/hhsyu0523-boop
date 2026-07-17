from __future__ import annotations

from itertools import product
from pathlib import Path
import random

from src.common.io import load_latest_csv
from src.engines.base import BaseEngine


class NumbersEngine(BaseEngine):
    digits: int = 3

    def _extract_draws(self, df) -> list[str]:
        preferred = ["当選番号", "本数字", "numbers", "number", "result"]
        for col in preferred:
            if col in df.columns:
                return [str(v).split(".")[0].zfill(self.digits) for v in df[col].dropna()]

        for col in reversed(df.columns):
            values = df[col].dropna().astype(str)
            cleaned = [v.replace("-", "").replace(" ", "") for v in values]
            valid = [v.zfill(self.digits) for v in cleaned if v.isdigit() and len(v) <= self.digits]
            if valid:
                return valid
        raise ValueError("当選番号の列を自動判定できませんでした。")

    def predict(self, data_path: Path, count: int) -> list[str]:
        df = load_latest_csv(data_path)
        draws = self._extract_draws(df)
        recent = draws[-200:]

        position_freq = []
        for pos in range(self.digits):
            freq = {str(d): 1 for d in range(10)}
            for value in recent:
                freq[value[pos]] += 1
            position_freq.append(freq)

        candidates = []
        for digits in product("0123456789", repeat=self.digits):
            value = "".join(digits)
            score = sum(position_freq[i][d] for i, d in enumerate(digits))

            unique_count = len(set(digits))
            if unique_count == self.digits:
                score += 4
            elif unique_count == self.digits - 1:
                score += 2

            candidates.append((score, value))

        random.Random(13).shuffle(candidates)
        candidates.sort(reverse=True)

        selected: list[str] = []
        for _, value in candidates:
            if value in selected:
                continue
            selected.append(value)
            if len(selected) >= count:
                break
        return selected


class Numbers3Engine(NumbersEngine):
    game_key = "numbers3"
    display_name = "Numbers3"
    digits = 3


class Numbers4Engine(NumbersEngine):
    game_key = "numbers4"
    display_name = "Numbers4"
    digits = 4
