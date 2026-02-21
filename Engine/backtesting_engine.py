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
                sl_price = getattr(self.strategy, 'get_sl_price', lambda: None)()
                status = self.portfolio.update(signal, executed_price, sl_price=sl_price)
            else:
                # VERY IMPORTANT:
                # still check stop loss / take profit
                status = self.portfolio.update(None, price)

            # SYNC Strategy position if portfolio closed it (SL)
            if status == "CLOSED" and self.strategy.position == 1:
                # Use duck typing or check if method exists
                if hasattr(self.strategy, 'sync_position'):
                    self.strategy.sync_position(0)
                else:
                    self.strategy.position = 0

            # Clean equity calculation
            equity = self.portfolio.get_equity(price)
            self.metrics.update_equity(equity)