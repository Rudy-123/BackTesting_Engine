import matplotlib.pyplot as plt
from pathlib import Path

def compute_drawdown(equity_curve):
    drawdowns = []
    peak = equity_curve[0]

    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (value - peak) / peak
        drawdowns.append(drawdown)

    return drawdowns


def plot_equity_curve(strategy_id, equity_curve):
    Path("results/plots").mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(equity_curve)
    plt.xlabel("Time")
    plt.ylabel("Equity Value")
    plt.title(f"Equity Curve — {strategy_id}")
    plt.savefig(f"results/plots/{strategy_id}_equity.png")
    plt.close()


def plot_drawdown_curve(strategy_id, drawdowns):
    Path("results/plots").mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(drawdowns)
    plt.xlabel("Time")
    plt.ylabel("Drawdown")
    plt.title(f"Drawdown Curve — {strategy_id}")
    plt.savefig(f"results/plots/{strategy_id}_drawdown.png")
    plt.close()
