class BaseStrategy:
    def __init__(self):
        self.position=0 #Trade open or not 0=open 1=buy done (long position)

    def on_candle(self,candle):
        #Called on every candle must return buy,sell,hold
        raise NotImplementedError
    