class Metrics:
    def __init__(self,starting_capital):
        self.starting_capital=starting_capital
        self.equity_curve=[]
        self.trades=[]

    def record_trade(self,pnl):
        self.trades.append(pnl)

    def update_equity(self,current_equity):
        self.equity_curve.append(current_equity)

    def summary(self):
        total_pnl=sum(self.trades) #net result of all trades
        total_trades=len(self.trades)
        wins=len([p for p in self.trades if p>0])  #how many profitable trades
        win_rate=(wins/total_trades)*100 if total_trades>0 else 0
        max_drawdown=self.max_drawdown()

        return {
            "total_pnl": float(total_pnl),
            "total_trades": int(total_trades),
            "win_rate": float(round(win_rate, 2)),
            "max_drawdown": float(round(-max_drawdown, 2)),
            "equity_curve": list(self.equity_curve)
        }


    def max_drawdown(self):     
        peak=self.starting_capital
        max_dd=0
        for equity in self.equity_curve:
            if equity>peak:
                peak=equity #update new peak if found
            drawdown=peak-equity #find the steep
            max_dd=max(max_dd,drawdown)
        return max_dd