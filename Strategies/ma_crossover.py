from Strategies.basic_strategy import BaseStrategy
class MACrossoverStrategy(BaseStrategy):
    def __init__(self,short_window=5,long_window=15,ema_period=200):
        BaseStrategy.__init__(self) 
        self.short_window=short_window
        self.long_window=long_window
        self.ema_period=ema_period
        self.ema=None  #running EMA for trend filter
        self.prices=[] #stores the closing prices of candles

    def on_candle(self,candle):
        close_price=candle["close"]
        self.prices.append(close_price)

        #Update EMA (exponential moving average for trend filter)
        if self.ema is None:
            self.ema=close_price
        else:
            k=2/(self.ema_period+1)
            self.ema=close_price*k+self.ema*(1-k)

        #while we dont hv enough data nothing to be done
        if len(self.prices)<self.long_window:
            return "HOLD"
        short_ma=sum(self.prices[-self.short_window:])/self.short_window
        long_ma=sum(self.prices[-self.long_window:])/self.long_window

        #BUY only when trending up (price above EMA200) + momentum strength filter
        if (short_ma>long_ma and self.position==0 and close_price>self.ema
                and abs(short_ma-long_ma)/close_price>0.001):
            self.position=1
            return "BUY"
        #SELL on reverse crossover (long-only, no shorting)
        if long_ma>short_ma and self.position==1:
            self.position=0
            return "SELL"
        return "HOLD"