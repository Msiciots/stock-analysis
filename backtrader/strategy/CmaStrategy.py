import backtrader as bt
from strategy.base import Base
# Create a Stratey
class CmaStrategy(Base):
    """
    Implementing the CMA_sta strategy from zwPython.

    Rule:
        While close and MA crossover:
            If MA trend is go up: buy.
            If MA trend is go down: sell.

    Args:
        maperiod (int): The time period for moving average.
    """

    params = (("maperiod", 15),)

    def __init__(self):

        # multiple inheritance
        super(CmaStrategy, self).__init__()

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

        # Check stock Trend
        trend = None
        ma, ma_lag2 = self.sma[0], self.sma[-2]
        close, close_lag2 = self.dataclose[0], self.dataclose[-2]
        if (close > ma) and (close_lag2 < ma_lag2) and (close > close_lag2):
            trend = 1
        elif (close < ma) and (close_lag2 > ma_lag2) and (close < close_lag2):
            trend = -1

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if trend == 1:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if trend == -1:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
