import backtrader as bt
from strategy.base import Base
# Create a Stratey
class SmaStrategy(Base):
    """
    Implementing the SMA_sta strategy from zwPython.

    Rule:
        If close price > SMA: buy
        If close price < SMA: sell

    Args:
        maperiod (int): The time period for moving average.
    """

    params = (("maperiod", 15),)

    def __init__(self):

        # multiple inheritance
        super(SmaStrategy, self).__init__()
        print("maperiod:", self.params.maperiod)

        # Add indicators
        self.sma = bt.indicators.SimpleMovingAverage(
            self.dataclose, period=self.params.maperiod
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log("Close, %.2f" % self.dataclose[0])
        self.log(
            "O:{:.2f}, H:{:.2f}, L:{:.2f}, C:{:.2f}".format(
                self.dataopen[0], self.datahigh[0], self.datalow[0], self.dataclose[0]
            )
        )

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()