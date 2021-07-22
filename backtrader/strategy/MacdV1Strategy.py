import backtrader as bt
from strategy.base import Base
# Create a Stratey
class MacdV1Strategy(Base):
    """
    Implementing the macd10 strategy from zwPython.

    Rule:
        If MACD > 0: buy.
        If MACD < 0: sell.

    Args:.
        fast_period (int): fast ema period.
        slow_period (int): slow ema period.
        signal_period (int): macd signal period.

    """

    params = (("fast_period", 12), ("slow_period", 26), ("signal_period", 9))

    def __init__(self):

        # multiple inheritance
        super(MacdV1Strategy, self).__init__()

        print("period_me1:", self.params.fast_period)
        print("period_me2:", self.params.slow_period)
        print("period_signal:", self.params.signal_period)

        # Add indicators
        self.macd = bt.indicators.MACD(
            self.dataclose,
            period_me1=self.params.fast_period,
            period_me2=self.params.slow_period,
            period_signal=self.params.signal_period,
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
            if self.macd.macd[0] > 0:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log("BUY CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            # self.mcross[0] == -1:
            if self.macd.macd[0] < 0:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()