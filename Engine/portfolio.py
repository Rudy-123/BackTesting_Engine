class Portfolio:
    def __init__(self, capital, metrics):
        self.initial_capital = capital
        self.cash = capital
        self.position = 0          # 0 = no position, 1 = long
        self.entry_price = None
        self.stop_price = None
        self.quantity = 0
        self.trades = []
        self.metrics = metrics

    def update(self, signal, price, sl_price=None):
        """
        signal: "BUY", "SELL", or None
        price: current market price
        sl_price: optional custom stop loss price
        Returns: "OPEN", "CLOSED", or None
        """

        # BUY      
        if signal == "BUY" and self.position == 0:

            if self.cash <= 0:
                return None

            self.quantity = self.cash / price
            self.entry_price = price
            self.stop_price = sl_price if sl_price else price * 0.98 # Fallback to 2%
            self.position = 1
            return "OPEN"

        # RISK MANAGEMENT
   
        if self.position == 1:
            # Stop Loss
            if price <= self.stop_price:
                pnl = self.quantity * (price - self.entry_price)
                self.cash += pnl
                self.trades.append(pnl)

                if self.metrics:
                    self.metrics.record_trade(pnl)

                self.position = 0
                self.entry_price = None
                self.quantity = 0
                self.stop_price = None
                return "CLOSED"

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
            return "CLOSED"
        
        return "OPEN" if self.position == 1 else None


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