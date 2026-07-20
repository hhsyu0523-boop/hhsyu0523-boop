from pathlib import Path

from config.settings import load_config
from prediction.predictor import PredictionOrchestrator


def test_smoke() -> None:
    config = load_config(Path("config/config.yaml"))
    orchestrator = PredictionOrchestrator(config=config)
    result = orchestrator.run_demo()

    assert result["project"] == "NumbersAI_Ver13"
    assert set(result["results"].keys()) == {"numbers3", "numbers4", "loto6", "loto7", "miniloto"}
