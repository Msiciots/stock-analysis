import backtrader as bt

class Base(bt.Strategy):
    """
    Define base Strategy class (main structure),
    so the class structure could remain consistent.
    All Strategy inherit this class.
    """
    params = (
        ('ma_period', 15),
        ('mode', ''),
        ('partrate', 0.2),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataclose = self.datas[0].close
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # self.datas[0].plotinfo.plotlinelabels = True
    def notify_order(self, order):
        if order.status in [order.Submitted,order.Accepted]:
            return
# self.broker.setcommission(commission=0.001425)
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '\033[1;31mBUY EXECUTED, Price: %.2f, Size: %.2f ,Cost: %.2f, Comm %.2f, Cash: %.2f, Value: %.2f, Hold size: %.2f\033[0m' %
                    (order.executed.price,
                    order.executed.size,
                     order.executed.value,
                     order.executed.comm,
                     self.broker.get_cash(),
                     self.broker.getvalue(),
                     self.position.size
                     ))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.gain = order.executed.price * order.executed.size * -1
                self.log('\033[1;32mSELL EXECUTED, Price: %.2f, Size: %.2f , Gain: %.2f, Comm %.2f, Tax %.2f\033[0m' %
                         (order.executed.price,
                         order.executed.size,
                          self.gain,
                          self.gain * 0.001428,
                        #   order.executed.comm,
                          self.gain * 0.003))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('\033[1;33mOPERATION PROFIT, GROSS %.2f, NET %.2f, RATE: %.2f, Cash: %.2f, Value: %.2f, Hold size: %.2f\033[0m' %
                 (trade.pnl, trade.pnlcomm,trade.pnlcomm/self.gain,self.broker.get_cash(),self.broker.getvalue(),self.position.size))
