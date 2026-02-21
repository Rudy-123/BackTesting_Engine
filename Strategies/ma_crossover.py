from Strategies.basic_strategy import BaseStrategy

class MACrossoverStrategy(BaseStrategy):
    def __init__(self, short_window=20, long_window=50, ema_period=200, atr_period=14):
        BaseStrategy.__init__(self) 
        self.short_window = short_window
        self.long_window = long_window
        self.ema_period = ema_period
        self.atr_period = atr_period
        
        self.prices = [] 
        self.highs = []
        self.lows = []
        
        self.ema = None
        self.ema_history = []
        self.atr = None
        self.atr_history = []
        self.prev_close = None
        self.sl_price = None
        
        # New: Tracking for strict crossover
        self.prev_sma_short = None
        self.prev_sma_long = None

    def calculate_rsi(self, period=14):
        if len(self.prices) < period + 1:
            return 50
        deltas = [self.prices[i] - self.prices[i-1] for i in range(-period, 0)]
        gains = [d for d in deltas if d > 0]
        losses = [-d for d in deltas if d < 0]
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def on_candle(self, candle):
        close_price = candle["close"]
        high_price = candle["high"]
        low_price = candle["low"]
        
        self.prices.append(close_price)
        self.highs.append(high_price)
        self.lows.append(low_price)

        # Update EMA 200
        if self.ema is None:
            self.ema = close_price
        else:
            k = 2 / (self.ema_period + 1)
            self.ema = close_price * k + self.ema * (1 - k)
        self.ema_history.append(self.ema)

        # Update ATR
        tr = high_price - low_price
        if self.prev_close is not None:
            tr = max(tr, abs(high_price - self.prev_close), abs(low_price - self.prev_close))
        
        if self.atr is None:
            self.atr = tr
        else:
            alpha = 1 / self.atr_period
            self.atr = alpha * tr + (1 - alpha) * self.atr
        self.atr_history.append(self.atr)
        
        self.prev_close = close_price

        # Wait for enough data
        if len(self.prices) < self.long_window + self.atr_period:
            return "HOLD"

        # Moving Averages
        sma_short = sum(self.prices[-self.short_window:]) / self.short_window
        sma_long = sum(self.prices[-self.long_window:]) / self.long_window
        
        # 1. EMA Slope Filter (Ensure long term trend is actually rising)
        ema_rising = False
        if len(self.ema_history) > 10:
            ema_rising = self.ema > self.ema_history[-10]

        # 2. ATR Volatility Filter (Avoid "Dead" non-moving markets)
        avg_atr = sum(self.atr_history[-20:]) / 20
        high_vol = self.atr > (0.8 * avg_atr)

        # 3. RSI Momentum (Ensure we aren't buying overextended or weak)
        rsi = self.calculate_rsi(14)
        bullish_momentum = 50 < rsi < 75

        # 4. Strict Crossover Logic
        cross_up = False
        if self.prev_sma_short is not None and self.prev_sma_long is not None:
            if self.prev_sma_short <= self.prev_sma_long and sma_short > sma_long:
                cross_up = True
        
        self.prev_sma_short = sma_short
        self.prev_sma_long = sma_long

        # BUY Condition: Strict Crossover + Trend Stack + Rising EMA + Volatility + RSI
        if (cross_up and sma_short > sma_long > self.ema 
                and ema_rising and high_vol and bullish_momentum 
                and self.position == 0):
            
            # Entry found - Set ATR based Stop Loss (2.5 * ATR for buffer)
            self.sl_price = close_price - (2.5 * self.atr)
            self.position = 1
            return "BUY"

        # EXIT Condition: Trend stack breaks OR Trailing Stop Hit (managed by portfolio)
        if (sma_long > sma_short) and self.position == 1:
            self.position = 0
            self.sl_price = None
            return "SELL"

        return "HOLD"

    def get_sl_price(self):
        return self.sl_price

    def sync_position(self, pos):
        self.position = pos
        if pos == 0:
            self.sl_price = None