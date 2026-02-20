class Portfolio:
    def __init__(self, capital, metrics):
        self.initial_capital = capital
        self.cash = capital
        self.position = 0          # 0 = no position, 1 = long
        self.entry_price = None
        self.quantity = 0
        self.trades = []
        self.metrics = metrics

    def update(self, signal, price):
        """
        signal: "BUY", "SELL", or None
        price: current market price
        """

        # BUY      
        if signal == "BUY" and self.position == 0:

            if self.cash <= 0:
                return

            self.quantity = self.cash / price
            self.entry_price = price
            self.position = 1
            return

        # RISK MANAGEMENT (STOP LOSS ONLY — no TP, let trends run)
   
        if self.position == 1:

            stop_price = self.entry_price * 0.98      # 2% Stop Loss

            # Stop Loss
            if price <= stop_price:
                pnl = self.quantity * (price - self.entry_price)
                self.cash += pnl
                self.trades.append(pnl)

                if self.metrics:
                    self.metrics.record_trade(pnl)

                self.position = 0
                self.entry_price = None
                self.quantity = 0
                return

        # SELL FROM STRATEGY SIGNAL
      
        if signal == "SELL" and self.position == 1:

            pnl = self.quantity * (price - self.entry_price)
            self.cash += pnl
            self.trades.append(pnl)

            if self.metrics:
                self.metrics.record_trade(pnl)

            self.position = 0
            self.entry_price = None
            self.quantity = 0


    def get_equity(self, current_price):
        """
        Returns total portfolio equity (cash + unrealized PnL)
        """
        equity = self.cash

        if self.position == 1:
            unrealized = self.quantity * (current_price - self.entry_price)
            equity += unrealized

        return equity


    def reset(self):
        """
        Reset portfolio state (useful for multi-strategy runs)
        """
        self.cash = self.initial_capital
        self.position = 0
        self.entry_price = None
        self.quantity = 0
        self.trades = []