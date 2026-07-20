from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AppConfig(dict):
    """Simple dictionary-based configuration wrapper."""


def load_config(path: Path | str) -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        return AppConfig(
            {
                "project_name": "NumbersAI_Ver13",
                "python_version": "3.12",
                "database": {"format": "csv", "path": "database"},
                "engines": ["numbers3", "numbers4", "loto6", "loto7", "miniloto"],
            }
        )

    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return AppConfig(data)
