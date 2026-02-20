from Engine.data_loader import DataLoader
from Engine.execution import ExecutionEngine
from Engine.portfolio import Portfolio
from Engine.metrics import Metrics
from Strategies.ma_crossover import MACrossoverStrategy

def build_jobs(config,strategy_params): #config->YAML se aaya hua pura exp plan and strategy params means the pairs generated for lwindow,swindow
    jobs=[]
    ema_period=config["strategies"]["ma_crossover"].get("ema_period",200)
    for short,long in strategy_params:
        strategy=MACrossoverStrategy(short,long,ema_period=ema_period)
        execution=ExecutionEngine(
            config["execution"]["commission"],
            config["execution"]["slippage"]
        )
        metrics = Metrics(config["portfolio"]["capital"])
        portfolio = Portfolio(config["portfolio"]["capital"], metrics)
        jobs.append((
            config["data"]["path"], #only path is passed
            execution,
            strategy,
            portfolio,
            metrics,
            short,
            long
        ))
    return jobs