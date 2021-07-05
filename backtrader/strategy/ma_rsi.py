from datetime import datetime
# Import the backtrader platform
import backtrader as bt
# Create a Stratey
class ma_rsi(bt.Strategy):
    """
    Entry:
        RSI > 50 and close price cross up the MA line
    Exit:
        Close price cross down the MA line
    Mode: allin, partial
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
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open  
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.initCash = self.broker.getvalue()
        self.gain = 0
        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.ma_period)
        # Add a RSI
        self.rsi = bt.indicators.RSI(self.datas[0])

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '\033[1;31mBUY EXECUTED, Price: %.2f, Size: %.2f ,Cost: %.2f, Comm %.2f, Cash: %.2f, Hold size: %.2f\033[0m' %
                    (order.executed.price,
                    order.executed.size,
                     order.executed.value,
                     order.executed.comm,
                     self.broker.get_cash(),
                     self.position.size))

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

    def next(self):
        # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        # Not yet ... we MIGHT BUY if ...
        if ( self.rsi[0] > 50 ) and (self.dataclose[0] > self.sma[0]) and (self.dataclose[-1] < self.sma[-1]):
            
            # BUY, BUY, BUY!!! (with all possible default parameters)

            self.broker.setcommission(commission=0.001425)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # self.log('current cash: %.2f , price: %.2f' % (self.broker.getvalue(),self.dataopen[0]))
            # Keep track of the created order to avoid a 2nd order

            # Default, fixed size
            if self.params.mode=='':
                self.order = self.buy()
            # partial in
            elif self.params.mode=='partial':
                size = (self.broker.getvalue() * self.params.partrate) // self.dataopen[1]
                self.order = self.buy(size=size)

            # All in
            elif self.params.mode=='allin':
                size1 = self.broker.get_cash() // self.dataopen[1]
                size2 = self.broker.get_cash() // self.dataclose[0]
                if size1 > size2:
                    size = size2
                else:
                    size = size1
                print("Cash: %.2f , nextOpen: %.2f" % (self.broker.get_cash(),self.dataopen[1]))
                self.order = self.buy(size=size)
            return

        if self.position:
            if (self.dataclose[0] < self.sma[0]) and (self.dataclose[-1] > self.sma[-1]):
                self.broker.setcommission(commission=0.001425+0.003)
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # self.log('current cash: %.2f , price: %.2f' % (self.broker.getvalue(),self.dataopen[0]))
                # Keep track of the created order to avoid a 2nd order
                # Default, fixed size
                if self.params.mode=='':
                    self.order = self.sell()
                # All out
                elif self.params.mode=='allin':
                    self.order = self.sell(size=self.position.size) 
                # partial out
                elif self.params.mode=='partial':
                    size = (self.broker.getvalue() * self.params.partrate ) // self.dataclose[0]
                    if size > self.position.size:
                        self.order = self.sell(size=self.position.size) 
                    else:
                        self.order = self.sell(size=size) 

                
