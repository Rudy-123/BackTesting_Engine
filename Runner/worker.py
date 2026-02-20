from Engine.data_loader import DataLoader
from Engine.datafeed import DataFeed
from Engine.backtesting_engine import BacktestingEngine

def run_single_backtest(args):
    data_path,execution,strategy,portfolio,metrics,short_w,long_w=args
    data=DataLoader().load_data(data_path) #Each worker loads it's data khudse
    feed=DataFeed(data)
    engine = BacktestingEngine(
        feed, execution, strategy, portfolio, metrics
    )
    engine.run()
    result=metrics.summary()
    result["strategy_id"]=f"ma_{short_w}_{long_w}"
    result["parameters"]={"short_window":short_w,"long_window":long_w}
    return result
