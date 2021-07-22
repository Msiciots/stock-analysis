import backtrader as bt
from strategy.base import Base
from strategy.utils import VolumeWeightedAveragePrice
# Create a Stratey
class VwapStrategy(Base):
    """
    Implementing the VWAP_sta strategy from zwPython.

    Rule:
        No description in the book.

    Args:
        maperiod (int): The time period for sliding window in VWAP.
        kvwap (float): threshold.
    """

    params = (("maperiod", 15), ("kvwap", 0.01))

    def __init__(self):

        # multiple inheritance
        super(VwapStrategy, self).__init__()

        print("maperiod:", self.params.maperiod)
        print("kvwap:", self.params.kvwap)

        # Add indicators
        self.vwap = VolumeWeightedAveragePrice(
            self.datas[0], period=self.params.maperiod
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
        vwap = self.vwap[0]
        if vwap > 0:
            close = self.dataclose[0]
            kvwap = self.params.kvwap
            stock_num = self.broker.getposition(self.datas[0]).size
            cash = self.broker.get_cash()
            stock_value = stock_num * close

            if not self.position:

                if (close > vwap * (1 + kvwap)) and (stock_value < (cash * 0.9)):

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log("BUY CREATE, %.2f" % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()

            else:

                if (close < vwap * (1 - kvwap)) and (stock_value > 0):

                    # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log("SELL CREATE, %.2f" % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()