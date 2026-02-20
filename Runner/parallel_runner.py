from multiprocessing import Pool
from Engine.backtesting_engine import BacktestingEngine

def run_single_backtest(args):
    datafeed, execution, strategy, portfolio, metrics, short_w, long_w = args
    
    engine=BacktestingEngine(   #Engine creation only for this process and no shared state so 1 process runs on all the candles on which strategy a is applied 
        datafeed, execution, strategy, portfolio, metrics
    )
    engine.run()
    result=metrics.summary()
    result["strategy_id"]=f"ma_{short_w}_{long_w}"
    result["parameters"]={"short_window":short_w,"long_window":long_w}
    return result

def run_parallel(jobs,workers=8):
    with Pool(processes=workers) as pool:
        results=pool.map(run_single_backtest,jobs)
    return results