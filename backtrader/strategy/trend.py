from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
# Import the backtrader platform
import backtrader as bt
from strategy.base import Base
# Create a Stratey
class trend(Base):
    """
    Entry:
        Close price break through the upper box ratio
    Exit:
        Close price break through the stop ratio
    """
    params = (
        ('box_ratio', 0.02),
        ('stop_ratio', 0.07),
    )

    def __init__(self):

        # multiple inheritance
        super(trend, self).__init__()

        self.start_price = None
        self.buy_price = None
        
        # Indicators for the plotting show
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

   
    def next(self):
        # Simply log the closing price of the series from the reference
        if not self.start_price:
            self.start_price = self.dataclose[0]
#         self.log('Start price, %.2f' % self.start_price)
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.start_price * (1+self.params.box_ratio) :
                
                
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
                
                self.buy_price = self.dataclose[0]
        else:

            if (self.dataclose[0] < self.buy_price * (1-self.params.stop_ratio))  or (self.dataclose[0] > self.buy_price * (1+self.params.stop_ratio)):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                
                self.start_price = self.dataclose[0]
