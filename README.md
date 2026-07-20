# NumbersAI_Ver13

NumbersAI_Ver13 is a modular Python 3.12 project for lottery prediction workflows. It now includes historical CSV data support, automatic validation, feature generation, training, backtesting, history tracking, evaluation reporting, and CLI commands.

## Features

- Historical CSV dataset support for Numbers3, Numbers4, MiniLoto, Loto6, and Loto7
- Automatic validation and cleaning
- Automatic feature generation
- Daily database updates
- Rolling backtesting
- Machine learning training workflow
- Prediction history and evaluation reports
- CLI commands for update, train, backtest, and predict

## Project Structure

- database/: CSV persistence and data management
- engine/: prediction engines
- learning/: feature engineering and training modules
- backtest/: backtesting utilities
- prediction/: orchestration, history, and reporting
- reports/: generated CSV reports
- logs/: logging helpers
- config/: YAML configuration
- tests/: automated tests

## Quick Start

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Run a daily update
   ```bash
   python main.py update
   ```
3. Train models
   ```bash
   python main.py train
   ```
4. Run a backtest
   ```bash
   python main.py backtest
   ```
5. Generate predictions
   ```bash
   python main.py predict
   ```

## Example Output

Prediction reports are written to CSV files in the reports/ directory.
