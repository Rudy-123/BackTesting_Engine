import time
from Runner.config_loader import load_config
from Runner.strategy_factory import generate_strategies
from Runner.job_builder import build_jobs
from Runner.batch_runner import run_batched

def benchmark():
    config = load_config("config/experiment.yaml")
    strategy_params = generate_strategies(config)
    jobs = build_jobs(config, strategy_params)

    start = time.time()
    results = run_batched(
        jobs,
        workers=config["parallel"]["workers"],
        batch_size=config["parallel"]["batch_size"]
    )
    end = time.time()

    total_time = end - start
    total_strategies = len(results)

    print("Total strategies:", total_strategies)
    print("Total time (sec):", round(total_time, 2))
    print("Avg time / strategy (sec):", round(total_time / total_strategies, 4))

if __name__ == "__main__":
    benchmark()
