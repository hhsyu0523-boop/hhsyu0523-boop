from __future__ import annotations
import pandas as pd
from typing import Any
from engine.numbers4_engine import Numbers4PredictionEngine
from backtest.rolling_backtest import RollingBacktest
from backtest.runner import BacktestRunner
from database.csv_store import CSVStore
from database.loader import DataLoader
from engine.loto6_engine import Loto6PredictionEngine
from engine.loto7_engine import Loto7PredictionEngine
from engine.miniloto_engine import MiniLotoPredictionEngine
from engine.numbers3_engine import Numbers3PredictionEngine
from learning.feature_engineering import FeatureEngineer
from learning.feature_pipeline import FeaturePipeline
from learning.ml_pipeline import SimpleMLPipeline
from learning.modeling import LotteryModelTrainer
from prediction.history_store import PredictionHistoryStore
from prediction.box_optimizer import create_box_ranking
from prediction.reporting import PredictionReportExporter


class PredictionOrchestrator:
    """High-level orchestrator for prediction workflows."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.engines = {
            "numbers3": Numbers3PredictionEngine(),
            "numbers4": Numbers4PredictionEngine(),
            "loto6": Loto6PredictionEngine(),
            "loto7": Loto7PredictionEngine(),
            "miniloto": MiniLotoPredictionEngine(),
        }
        self.feature_engineer = FeatureEngineer()
        self.feature_pipeline = FeaturePipeline()
        self.ml_pipeline = SimpleMLPipeline()
        self.model_trainer = LotteryModelTrainer()
        self.backtest = RollingBacktest()
        self.backtest_runner = BacktestRunner()
        self.store = CSVStore(self.config.get("database", {}).get("path", "database"))
        self.loader = DataLoader("database")
        self.history_store = PredictionHistoryStore("reports")
        self.report_exporter = PredictionReportExporter()

    def run_demo(self) -> dict[str, Any]:
        datasets = self.loader.load_all()
        results: dict[str, Any] = {}
        report_rows: list[dict[str, Any]] = []

        for name, engine in self.engines.items():
            history = datasets.get(name, pd.DataFrame(columns=["draw_date", "numbers", "game"])).to_dict(orient="records")
            result = engine.predict(history)
            results[name] = {
                "mode": result.mode,
                "predictions": result.predictions,
                "metadata": result.metadata,
            }

            for row in result.metadata.get("ranking", []):
                report_rows.append({
                    "engine": name,
                    "rank_type": row.get("rank_type", "box"),
                    "digits": row.get("digits", 3),
                    "combination": row.get("combination", []),
                    "score": row.get("score", 0),
                })

        self.store.save("predictions_demo", [{"engine": key, **value} for key, value in results.items()])
        self.history_store.save(
            [
                {
                    "game": key,
                    "engine": "box_priority",
                    "prediction": "-".join(str(item) for item in value.get("predictions", [])),
                    "score": 0,
                    "timestamp": "2026-07-17",
                }
                for key, value in results.items()
            ],
            filename="prediction_history.csv",
        )
        self.report_exporter.export(report_rows, "reports/prediction_report.csv")
        return {
            "project": self.config.get("project_name", "NumbersAI_Ver13"),
            "results": results,
            "backtest": self.backtest.run(datasets.get("numbers3", [])),
            "features": self.feature_engineer.feature_names,
            "report_path": "reports/prediction_report.csv",
            "history_path": "reports/prediction_history.csv",
        }

    def run_backtest(self) -> dict[str, Any]:
        datasets = self.loader.load_all()
        summary = {}
        for game, frame in datasets.items():
            history = frame.to_dict(orient="records")
            summary[game] = self.backtest_runner.run(history, window_size=20)
        self.report_exporter.export(
            [
                {
                    "engine": game,
                    "rank_type": "backtest",
                    "digits": 0,
                    "combination": [],
                    "score": summary[game]["rows"],
                }
                for game in summary
            ],
            "reports/backtest_report.csv",
        )
        return {"status": "completed", "summary": summary}

    def train_models(self) -> dict[str, Any]:
        datasets = self.loader.load_all()
        results = {}
        for game, frame in datasets.items():
            features = self.feature_pipeline.generate(frame)
            results[game] = self.model_trainer.train(features)
        self.report_exporter.export(
            [
                {
                    "engine": game,
                    "rank_type": "train",
                    "digits": 0,
                    "combination": [],
                    "score": results[game].get("accuracy", 0),
                }
                for game in results
            ],
            "reports/training_report.csv",
        )
        return {"status": "trained", "results": results}
if __name__ == "__main__":
    app = PredictionOrchestrator()

    print("=== Prediction Demo ===")
    demo = app.run_demo()
    print(demo)
print("\n=== Numbers4 Prediction ===")




loader = DataLoader("database")
datasets = loader.load_all()

engine = Numbers4PredictionEngine()

result = engine.predict(
    datasets["numbers4"].to_dict("records")
)

print("\n===== Numbers4 Ver.13 Prediction =====")

ranking = result.metadata.get("ranking", [])

for rank, item in enumerate(ranking[:15], start=1):
    combination = "".join(str(number) for number in item["combination"])
    score = item.get("score", 0)
    rank_type = item.get("rank_type", "unknown")

    print(
        f"{rank:02d}位  "
        f"{combination}  "
        f"{rank_type}  "
        f"score={score:.4f}"
    )


