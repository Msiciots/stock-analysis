import backtrader as bt
from strategy.base import Base
# Create a Stratey
class BBandsStrategy(Base):
    """
    Implementing the BBANDS_sta strategy from zwPython.
    Rule:
        If close price < bottom bband: sell.
        If close price > top bband: buy.
    Args:
        BBandsperiod (int): ma period
    """

    params = (("BBandsperiod", 20),)

    def __init__(self):

        # multiple inheritance
        super(BBandsStrategy, self).__init__()

        print("BBandsperiod:", self.params.BBandsperiod)

        # Add indicators
        self.bband = bt.indicators.BBands(
            self.dataclose, period=self.params.BBandsperiod
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log("Close, %.2f" % self.dataclose[0])
        # self.log(
        #     "O:{:.2f}, H:{:.2f}, L:{:.2f}, C:{:.2f}".format(
        #         self.dataopen[0], self.datahigh[0], self.datalow[0], self.dataclose[0]
        #     )
        # )

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        # if not self.position:
        if self.dataclose[0] < self.bband.lines.bot[0]:

            # BUY, BUY, BUY!!! (with all possible default parameters)
            self.log("BUY CREATE, %.2f" % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.broker.setcommission(commission=0.001425)
            self.order = self.buy()

        if self.position:
        # else:
            if self.dataclose[0] > self.bband.lines.top[0]:

                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.broker.setcommission(commission=0.001425+0.003)
                self.order = self.sell()
