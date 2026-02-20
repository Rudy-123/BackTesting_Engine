class DataFeed:
    def __init__(self,data):                
        self.data=data
        self.index=0 #current time position initially 0 
    
    def has_next(self):
        return self.index<len(self.data)
    
    def next_candle(self):
        candle=self.data.iloc[self.index]
        self.index+=1
        return candle

