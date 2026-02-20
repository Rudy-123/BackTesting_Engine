class ExecutionEngine:
    def __init__(self,commission_rate=0.001,slippage_rate=0.0005):
        self.commission_rate=commission_rate #commission=fees per trade
        self.slippage_rate=slippage_rate #the price impact
    
    def execute(self,signal,price):#signal tells buy or sell
        if signal=="BUY": #add the slippage as little more than expected
            executed_price=price*(1+self.slippage_rate)
            fee=executed_price*self.commission_rate
            return executed_price+fee
        elif signal=="SELL":
            executed_price=price*(1-self.slippage_rate)
            fee=executed_price*self.commission_rate
            return executed_price-fee
        return None 