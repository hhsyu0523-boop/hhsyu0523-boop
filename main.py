from __future__ import annotations

import sys
from pathlib import Path

from config.settings import load_config
from database.sample_data import SampleDataGenerator
from prediction.predictor import PredictionOrchestrator


def main() -> None:
    config = load_config(Path("config/config.yaml"))
    command = sys.argv[1] if len(sys.argv) > 1 else "predict"

    if command == "update":
        generator = SampleDataGenerator(config.get("database", {}).get("path", "database"))
        created = generator.generate()
        print({game: str(path) for game, path in created.items()})
        return

    if command == "train":
        orchestrator = PredictionOrchestrator(config=config)
        result = orchestrator.train_models()
        print(result)
        return

    if command == "backtest":
        orchestrator = PredictionOrchestrator(config=config)
        result = orchestrator.run_backtest()
        print(result)
        return

    if command == "predict":
        orchestrator = PredictionOrchestrator(config=config)
        result = orchestrator.run_demo()

        print("\n========== Prediction ==========\n")

        results = result.get("results", {})

        for game, values in results.items():
            print(values)
            print(f"\n【{game.upper()}】")

            ranking = values.get("metadata", {}).get("ranking", [])

            for i, item in enumerate(ranking[:20], start=1):
                combo = "".join(map(str, item["combination"]))
                score = round(item["score"], 3)

                print(f"{i:02d}. {combo}   score={score}")

    print("\n================================")

    return

    print("Unknown command. Use: update, train, backtest, predict")


if __name__ == "__main__":
    main()
