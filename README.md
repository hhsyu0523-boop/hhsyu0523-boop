# Lottery AI Prediction System Ver.13 Ultimate

宝くじ予測ロジックを、予想・検証・改善・履歴管理まで一体化する開発プロジェクトです。

## 対応対象

- Numbers3
- Numbers4
- ミニロト
- ロト6
- ロト7

## Ver.13 Phase 1

Phase 1では、今後の開発を継続できる土台を実装しています。

- 共通設定
- CSV読み込み
- Numbers3予想エンジンの初期版
- Numbers4 BOX優先エンジンの初期版
- 予想結果のJSON保存
- ローリングバックテストの雛形
- GitHub Actionsによる動作確認
- pytestによる基本テスト

## フォルダ構成

```text
.
├── .github/workflows/
├── backtest/
├── config/
├── data/
├── database/
├── prediction/
├── reports/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## セットアップ

```bash
python -m pip install -r requirements.txt
```

## 実行例

Numbers4を15口生成します。

```bash
python main.py predict --game numbers4 --count 15
```

Numbers3を15口生成します。

```bash
python main.py predict --game numbers3 --count 15
```

CSVを指定して実行します。

```bash
python main.py predict --game numbers4 --data data/numbers4.csv --count 15
```

結果は `reports/` にJSON形式で保存されます。

## CSV形式

Numbers4の例:

```csv
draw_no,date,number
7025,2026-07-13,1234
7026,2026-07-14,5678
```

Numbers3の例:

```csv
draw_no,date,number
7025,2026-07-13,123
7026,2026-07-14,567
```

`number` は先頭ゼロを保持するため、文字列として扱います。

## 現在の開発方針

Numbers4はBOX第一優先です。

- BOX候補を先に選定
- 桁別出現率を加点
- 直近傾向を加点
- 数字の偏りを抑制
- ダブル候補を別枠で確保
- 同一BOXの重複を抑制

Numbers3は次の配分を基本とします。

- シングル12口
- ダブル3口

## 注意

このシステムは過去データに基づく分析・検証用です。
当選を保証するものではありません。

## Version

- Current: Ver.13 Ultimate Phase 1
