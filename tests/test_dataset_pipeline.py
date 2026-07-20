from pathlib import Path

import pandas as pd

from database.dataset import HistoricalDataset
from learning.feature_pipeline import FeaturePipeline


def test_dataset_pipeline(tmp_path: Path) -> None:
    dataset = HistoricalDataset(tmp_path)
    frame = pd.DataFrame(
        [{"draw_date": "2026-07-01", "numbers": [1, 2, 3], "game": "numbers3"}]
    )
    validated = dataset.validate(frame)
    assert not validated.empty
    features = FeaturePipeline().generate(validated)
    assert "number_count" in features.columns
