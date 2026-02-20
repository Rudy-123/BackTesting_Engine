import json
import csv
from pathlib import Path

def save_run_result(result):
    Path("results/runs").mkdir(parents=True, exist_ok=True)
    with open(f"results/runs/{result['strategy_id']}.json", "w") as f:
        json.dump(result, f, indent=4)


def append_summary(result):
    summary_file = "results/summary.csv"
    file_exists = Path(summary_file).exists()

    params = result.get("parameters", {})

    short_window = params.get("short_window", "")
    long_window = params.get("long_window", "")

    with open(summary_file, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "strategy_id",
                "short_window",
                "long_window",
                "total_pnl",
                "max_drawdown",
                "win_rate",
                "trades"
            ])

        writer.writerow([
            result["strategy_id"],
            short_window,
            long_window,
            result["total_pnl"],
            result["max_drawdown"],
            result["win_rate"],
            result["total_trades"]
        ])
