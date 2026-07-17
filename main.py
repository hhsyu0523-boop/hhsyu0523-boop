from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from prediction.numbers3_engine import Numbers3Engine
from prediction.numbers4_engine import Numbers4Engine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lottery AI Prediction System Ver.13 Ultimate"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    predict = subparsers.add_parser("predict", help="予想を生成します")
    predict.add_argument(
        "--game",
        choices=["numbers3", "numbers4"],
        required=True,
        help="対象ゲーム",
    )
    predict.add_argument("--data", type=Path, default=None, help="CSVファイル")
    predict.add_argument("--count", type=int, default=15, help="生成口数")
    predict.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="結果保存先",
    )
    return parser


def run_prediction(game: str, data: Path | None, count: int) -> dict:
    if count <= 0:
        raise ValueError("countは1以上にしてください。")

    if game == "numbers4":
        engine = Numbers4Engine()
    elif game == "numbers3":
        engine = Numbers3Engine()
    else:
        raise ValueError(f"未対応ゲームです: {game}")

    if data is not None:
        engine.load_csv(data)

    predictions = engine.predict(count=count)
    return {
        "version": "Ver.13 Ultimate Phase 1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "game": game,
        "count": len(predictions),
        "predictions": predictions,
        "data_source": str(data) if data else "built-in fallback",
    }


def save_report(result: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"{result['game']}_{timestamp}.json"
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "predict":
        result = run_prediction(args.game, args.data, args.count)
        output_path = save_report(result, args.output_dir)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n保存先: {output_path}")


if __name__ == "__main__":
    main()
