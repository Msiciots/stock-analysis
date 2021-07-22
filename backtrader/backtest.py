from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
import json
from argparse import ArgumentParser
import os
# Import the backtrader platform
import backtrader as bt
import yfinance as yf
# Import the self-defined strategy
# from strategy.ma_rsi import ma_rsi 
from strategy import * 

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (30, 18)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input",help='The backtest config file.')
    parser.add_argument("-o", "--output-path", dest="output",help='The backtest output directory path.')
    args_cmd = parser.parse_args()
    f = open (args_cmd.input, "r")
    conf = json.load(f)
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    stname = conf['strategy']['name']
    stname = stname+'.'+stname
    args = ""
    for k, v in conf['strategy'].items():
        if k != 'name':
            args = args+","+k+"="+v
    str_addstrategy = "cerebro.addstrategy("+stname+args+")"
    exec(str_addstrategy)

    # Add a Sizer
    sname = conf['stake']['mode']
    args = ""
    for k, v in conf['stake'].items():
        if k != 'mode':
            args = args+","+k+"="+v
    str_addsizer = "cerebro.addsizer(bt.sizers."+sname+args+")"
    exec(str_addsizer)
    
    # cerebro.addsizer(bt.sizers.FixedSize, stake=50)
    # cerebro.addstrategy(eval(si))
    # cerebro.addstrategy(ma_rsi.ma_rsi,ma_period=15)
    # # cerebro.addsizer(bt.sizers.FixedSize, stake=50)
    # # cerebro.addsizer(bt.sizers.AllInSizerInt)
    # cerebro.addsizer(bt.sizers.PercentSizerInt, percents=20)
    # # cerebro.addstrategy(ma_rsi,ma_period=15,mode='allin')
    # # cerebro.addstrategy(ma_rsi,ma_period=15,mode='partial',partrate=0.2)
    
    # Add the Data Feed to Cerebro
    # data = bt.feeds.YahooFinanceData(dataname='2330.TW', fromdate=datetime(2020, 1, 1),todate=datetime(2020, 12, 31))
    # data = bt.feeds.PandasData(dataname=yf.download(conf['stockid'],conf['start'],conf['end']))
    # data = bt.feeds.PandasData(dataname=yf.download('2330.TW', '2018-01-01', '2019-01-01'))
    datapath = "./sample_data/600401_yahoo.csv"
    data = bt.feeds.YahooFinanceData(dataname=datapath, fromdate=datetime(2015, 1, 1),todate=datetime(2015, 12, 31),reverse=True,)
    cerebro.adddata(data)
    
    # Set our desired cash start
    cerebro.broker.setcash(conf['cash'])

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()
    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Plot the result
    cerebro.plot()
    # save the plot
    if not os.path.isdir(args_cmd.output):
        os.mkdir(args_cmd.output)
    plt.savefig(args_cmd.output+"/"+conf['stockid']+"_"+conf['strategy']['name']+"_"+conf['start']+"_"+conf['end']+".png", bbox_inches="tight")