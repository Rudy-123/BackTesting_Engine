class BacktestingEngine:
    def __init__(self, datafeed, execution, strategy, portfolio, metrics):
        self.datafeed = datafeed
        self.strategy = strategy
        self.execution = execution
        self.portfolio = portfolio
        self.metrics = metrics

    def run(self):

        while self.datafeed.has_next():

            candle = self.datafeed.next_candle()
            signal = self.strategy.on_candle(candle)
            price = candle["close"]

            # Execute order if signal
            if signal in ("BUY", "SELL"):
                executed_price = self.execution.execute(signal, price)
                self.portfolio.update(signal, executed_price)
            else:
                # VERY IMPORTANT:
                # still check stop loss / take profit
                self.portfolio.update(None, price)

            # Clean equity calculation
            equity = self.portfolio.get_equity(price)
            self.metrics.update_equity(equity)