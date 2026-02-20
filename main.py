import time
from pathlib import Path

from Runner.config_loader import load_config
from Runner.strategy_factory import generate_strategies
from Runner.job_builder import build_jobs
from Runner.batch_runner import run_batched

from reporting.result_writer import save_run_result, append_summary
from reporting.plots import (
    compute_drawdown,
    plot_equity_curve,
    plot_drawdown_curve
)
from reporting.analytics import enrich_summary


STARTING_CAPITAL = 100000
DATA_PATH = r"C:\Resume_Projects\Backtesting_Engine\data\raw\sample_data.csv"


def main():
    
    # Load config

    config = load_config("config/experiment.yaml")

    # Generate strategies
    strategy_params = generate_strategies(config)

    # Build jobs
    jobs = build_jobs(config, strategy_params)

    # Run batched jobs

    start = time.time()
    results = run_batched(
        jobs,
        workers=config["parallel"]["workers"],
        batch_size=config["parallel"]["batch_size"]
    )
    end = time.time()

    # DEBUG COUNTS (VERY IMPORTANT)

    print("Total strategies run:", len(results))
    print("Total backtest time:", round(end - start, 2), "seconds")

    # Reporting pipeline
    for result in results:

        # outputs
        save_run_result(result)
        append_summary(result)

        # plots
        drawdowns = compute_drawdown(result["equity_curve"])
        plot_equity_curve(result["strategy_id"], result["equity_curve"])
        plot_drawdown_curve(result["strategy_id"], drawdowns)

    #enrich summary ONCE
    if results:
        enrich_summary()


if __name__ == "__main__":
    main()
