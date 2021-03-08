import sys
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
import talib
if __name__ == "__main__":

    # Read argv from command
    sid = sys.argv[1]
    yf.pdr_override()
    start = sys.argv[2]
    end = sys.argv[3]
    
    # Get data from yfinance to dataframe
    df = yf.download(sid+'.TW', start, end)
    df = pd.DataFrame(data = df)

    # Calculate indexes
    sma_10 = talib.SMA(df['Close'], timeperiod=10)
    ema_24 = talib.EMA(df['Close'], timeperiod=24)
    adx_14 = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14 )
    macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    upperband, middleband, lowerband = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

########### Plot average figure ###########
    fig = plt.figure(figsize=(30, 10))
    ax = fig.add_axes([0.02,0.3,1,0.5])
    ax2 = fig.add_axes([0.02,0.1,1,0.2])
    # Plot average line
    ax.set_xticks(range(0, len(df.index), 10))
    ax.set_xticklabels(df.index[::10])

    mpf.plot(df,type='candle')

    ax.plot(sma_10, label='sma')
    ax.plot(ema_24, label='ema')
    ax.plot(adx_14, label='adx')
    ax.grid(True)
    ax.set_title('Average Line')
    ax.legend(loc='upper left', shadow=True, fontsize='x-large')
    # Plot Volume bar
    ax2 = df['Volume'].plot(kind='bar', color='k', alpha=0.3)
    x_labels = df.index.strftime('%Y/%m')
    ax2.set_xticklabels(x_labels,rotation=45)
    ax2.set_xticks(range(0, len(df.index), 10))
    ax2.set_title('Volume')
    ax2.grid(True)

    fig.subplots_adjust(hspace=0)
    fig.savefig('average_line.png')
   
########### Plot macd figure ###########
    fig2 = plt.figure(figsize=(30, 10))
    ax = fig2.add_axes([0.02,0.4,1,0.5])
    ax2 = fig2.add_axes([0.02,0.3,1,0.2])
    ax3 = fig2.add_axes([0.02,0.1,1,0.2])

    ax.set_xticks(range(0, len(df.index), 10))
    ax.set_xticklabels(df.index[::10])
    
    ax.plot(macd, label='macd')
    ax.grid(True)
    ax.legend(loc='upper left', shadow=True, fontsize='x-large')
    ax.set_title('MACD')

    ax2.plot(macdsignal, label='signal')
    ax2.plot(macdhist, label='macdhist')
    ax2.grid(True)
    ax2.legend(loc='upper left', shadow=True, fontsize='x-large')
    ax2.set_title('Sig & Hist')

    ax3 = df['Volume'].plot(kind='bar', color='k', alpha=0.3)
    ax3.set_xticklabels(x_labels,rotation=45)
    ax3.set_xticks(range(0, len(df.index), 10))
    ax3.set_title('Volume')
    ax3.grid(True)

    fig2.subplots_adjust(hspace=0)
    fig2.savefig('macd.png')

########### Plot bband figure ###########

    fig3 = plt.figure(figsize=(30, 10))
    ax = fig3.add_axes([0.02,0.3,1,0.5])
    ax2 = fig3.add_axes([0.02,0.1,1,0.2])

    ax.set_xticks(range(0, len(df.index), 10))
    ax.set_xticklabels(df.index[::10])
    ax.plot(upperband, label='upper')
    ax.plot(middleband, label='middle')
    ax.plot(lowerband, label='lower')
    ax.fill_between(df.index, upperband, lowerband, alpha=0.3 ,color='k')
    ax.set_title('BBAND')
    ax.grid(True)
    ax.legend(loc='upper left', shadow=True, fontsize='x-large')

    ax2 = df['Volume'].plot(kind='bar', color='k', alpha=0.3)
    ax2.set_xticklabels(x_labels,rotation=45)
    ax2.set_xticks(range(0, len(df.index), 10))
    ax2.set_title('Volume')
    ax2.grid(True)

    fig3.subplots_adjust(hspace=0)
    fig3.savefig('bband.png')