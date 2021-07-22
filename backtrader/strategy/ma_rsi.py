import backtrader as bt
from strategy.base import Base
# Create a Stratey
class ma_rsi(Base):
    """
    Rule:
        Buy: RSI > 50 and close price cross up the MA line 
        Sell: Close price cross down the MA line
    Args:
        ma_period: The sma day interval.
    """
    params = (
        ('ma_period', 15),
    )

    def __init__(self):
        # multiple inheritance
        super(ma_rsi, self).__init__()

        self.gain = 0
        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.ma_period)
        # Add a RSI
        self.rsi = bt.indicators.RSI(self.datas[0])

    def next(self):
        # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        # Not yet ... we MIGHT BUY if ...
        if ( self.rsi[0] > 50 ) and (self.dataclose[0] > self.sma[0]) and (self.dataclose[-1] < self.sma[-1]):
            
            # BUY, BUY, BUY!!! (with all possible default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            self.order = self.buy()
              

        if self.position:
            if (self.dataclose[0] < self.sma[0]) and (self.dataclose[-1] > self.sma[-1]):
            
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()


                
