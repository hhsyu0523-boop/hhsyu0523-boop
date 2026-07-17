from __future__ import annotations

from itertools import combinations
from pathlib import Path
import random
import re

from src.common.io import load_latest_csv
from src.engines.base import BaseEngine


class LotoEngine(BaseEngine):
    pick_count: int = 6
    max_number: int = 43

    def _extract_rows(self, df) -> list[list[int]]:
        rows: list[list[int]] = []
        for _, row in df.iterrows():
            nums: list[int] = []
            for value in row.tolist():
                if value is None:
                    continue
                for token in re.findall(r"\d+", str(value)):
                    n = int(token)
                    if 1 <= n <= self.max_number:
                        nums.append(n)
            unique = []
            for n in nums:
                if n not in unique:
                    unique.append(n)
            if len(unique) >= self.pick_count:
                rows.append(sorted(unique[: self.pick_count]))
        if not rows:
            raise ValueError("本数字を自動判定できませんでした。")
        return rows

    def predict(self, data_path: Path, count: int) -> list[str]:
        df = load_latest_csv(data_path)
        rows = self._extract_rows(df)
        recent = rows[-300:]

        freq = {n: 1 for n in range(1, self.max_number + 1)}
        for row in recent:
            for n in row:
                freq[n] += 1

        rng = random.Random(13)
        pool = list(range(1, self.max_number + 1))
        candidates: list[tuple[float, tuple[int, ...]]] = []

        for _ in range(20000):
            nums = tuple(sorted(rng.sample(pool, self.pick_count)))
            score = sum(freq[n] for n in nums)

            low = sum(n <= self.max_number / 3 for n in nums)
            mid = sum(self.max_number / 3 < n <= 2 * self.max_number / 3 for n in nums)
            high = self.pick_count - low - mid
            score -= max(low, mid, high) * 1.5

            odd = sum(n % 2 for n in nums)
            score -= abs(odd - self.pick_count / 2)

            candidates.append((score, nums))

        candidates.sort(reverse=True)
        selected: list[tuple[int, ...]] = []
        for _, nums in candidates:
            if any(len(set(nums) & set(existing)) >= self.pick_count - 1 for existing in selected):
                continue
            selected.append(nums)
            if len(selected) >= count:
                break

        return [" ".join(f"{n:02d}" for n in nums) for nums in selected]


class Loto6Engine(LotoEngine):
    game_key = "loto6"
    display_name = "Loto6"
    pick_count = 6
    max_number = 43


class Loto7Engine(LotoEngine):
    game_key = "loto7"
    display_name = "Loto7"
    pick_count = 7
    max_number = 37


class MiniLotoEngine(LotoEngine):
    game_key = "miniloto"
    display_name = "Mini Loto"
    pick_count = 5
    max_number = 31
