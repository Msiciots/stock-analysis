import backtrader as bt
from strategy.base import Base
# Create a Stratey
class TurStrategy(Base):
    """
    Implementing the tur10 strategy from zwPython.

    Rule:
        If close price > max( high price of pass n days): buy.
        After buy action, if close price < min( low proce of pass n day): sell

    Args:
        n_high(int): highest high price of pass n day.
        n_low(int): lowest low price of pass n day.

    """

    params = (("n_high", 30), ("n_low", 15))

    def __init__(self):

        # multiple inheritance
        super(TurStrategy, self).__init__()

        print("n_high:", self.params.n_high)
        print("n_low:", self.params.n_low)

        # Add indicators
        self.pass_highest = bt.indicators.Highest(
            self.datahigh, period=self.params.n_high
        )

        self.pass_lowest = bt.indicators.Lowest(self.datalow, period=self.params.n_low)

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
            if self.dataclose[0] > self.pass_highest[-1]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.pass_lowest[-1]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()