import backtrader as bt
from strategy.base import Base
# Create a Stratey
class KdjV1Strategy(Base):
    """
    Implementing the kdj10 strategy from zwPython.

    Rule:
        If K value > 90: buy.
        If K value < 10: sell.

    Args:
        period_dfast (int): EMA period in D value.

    """

    params = (("period_dfast", 3),)

    def __init__(self):

        # multiple inheritance
        super(KdjV1Strategy, self).__init__()

        print("printlog:", self.params.printlog)
        print("period_dfast:", self.params.period_dfast)

        # Add indicators
        self.kd = bt.indicators.StochasticFast(
            self.datas[0],
            period=1,
            period_dfast=self.params.period_dfast,
            movav=bt.indicators.EMA,
            safediv=True,
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
            if self.kd.percK[0] > 90:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

                print(self.kd.percK[0])
                print("=" * 25)

        else:

            if self.kd.percK[0] < 10:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()