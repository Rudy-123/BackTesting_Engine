import csv
from pathlib import Path

SUMMARY_FILE = "results/summary.csv"


def enrich_summary():
    if not Path(SUMMARY_FILE).exists():
        return

    with open(SUMMARY_FILE, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Derived metrics
    for row in rows:
        pnl = float(row["total_pnl"])
        trades = int(row["trades"])
        dd = abs(float(row["max_drawdown"]))

        row["pnl_per_trade"] = pnl / trades if trades > 0 else 0
        row["pnl_to_dd_ratio"] = pnl / dd if dd > 0 else 0

    # Ranking
    rows.sort(key=lambda x: float(x["total_pnl"]), reverse=True)
    for i, row in enumerate(rows):
        row["rank_by_pnl"] = i + 1

    rows.sort(key=lambda x: abs(float(x["max_drawdown"])))
    for i, row in enumerate(rows):
        row["rank_by_drawdown"] = i + 1

    # Write back enriched CSV
    fieldnames = rows[0].keys()

    with open(SUMMARY_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
