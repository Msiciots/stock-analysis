import backtrader as bt
from strategy.base import Base
# Create a Stratey
class RsiStrategy(Base):
    """
    Implementing the rsi10 strategy from zwPython.

    Rule:
        If rsi > kbuy: buy.
        If rsi < ksell: sell.

    Args:
        period (int): period for calucate rsi.
        kbuy (int): buy threshold for rsi value.
        ksell (int): sell threshold for rsi value.

    """

    params = (("period", 14), ("kbuy", 80), ("ksell", 20))

    def __init__(self):

        # multiple inheritance
        super(RsiStrategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("period:", self.params.period)
        print("kbuy:", self.params.kbuy)
        print("ksell:", self.params.ksell)

        # Add indicators
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.dataclose,
            period=self.params.period,
            movav=bt.indicators.EMA,
            safediv=False,
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
            if self.rsi[0] > self.params.kbuy:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.rsi[0] < self.params.ksell:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()