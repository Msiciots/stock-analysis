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
    plus_di = talib.PLUS_DI(df['High'], df['Low'], df['Close'], timeperiod=14 )
    minus_di = talib.MINUS_DI(df['High'], df['Low'], df['Close'], timeperiod=14 )
    macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    ema_12 = talib.EMA(df['Close'], timeperiod=12)
    ema_26 = talib.EMA(df['Close'], timeperiod=26)
    upperband, middleband, lowerband = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

    # plot sma, ema 
    apds = [mpf.make_addplot(sma_10,color='lime'),
            mpf.make_addplot(ema_24,color='c'),
        ]
    fig, axes=mpf.plot(df,type='candle',addplot=apds,returnfig=True,figscale=1.5,figratio=(16,9),title='\nAverage line',
            style='yahoo',volume=True)
    axes[0].legend(['sma_24','ema_24'])
    fig.savefig('Average line.png')

    # plot adx
    apds = [mpf.make_addplot(adx_14,color='r'),
            mpf.make_addplot(plus_di,color='lime'),
            mpf.make_addplot(minus_di,color='c')
            
        ]

    fig, axes=mpf.plot(df,type='candle',addplot=apds,returnfig=True,figscale=1.5,figratio=(16,9),title='\nADX',
            style='yahoo',volume=True,savefig=dict(fname='tsave300.jpg',dpi=100,pad_inches=0.25))
    axes[1].legend(['adx','di+','di-'])
    fig.savefig('adx.png')
    # plot macd
    apds = [mpf.make_addplot(ema_12,color='lime'),
            mpf.make_addplot(ema_26,color='c'),
            mpf.make_addplot(macdhist,type='bar',width=0.7,panel=1,
                            color='dimgray',alpha=1,secondary_y=False),
            mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=True),
            mpf.make_addplot(macdsignal,panel=1,color='b',secondary_y=True),
        ]

    fig, axes=mpf.plot(df,type='candle',addplot=apds,returnfig=True,figscale=1.5,figratio=(16,9),title='\nMACD',
            style='yahoo',volume=True,volume_panel=2,panel_ratios=(6,3,2),savefig=dict(fname='tsave100.jpg',dpi=100,pad_inches=0.25))
    axes[0].legend(['ema_12','ema_26'])
    axes[2].legend(['hist','macd','signal'])
    axes[3].legend(['macd','signal'])
    fig.savefig('macd.png')
    
    # plot bband
    apds = [mpf.make_addplot(upperband,color='lime'),
            mpf.make_addplot(middleband,color='r'),
            mpf.make_addplot(lowerband,color='b')
            
        ]

    fig, axes=mpf.plot(df,type='candle',addplot=apds,returnfig=True,figscale=1.5,figratio=(16,9),title='\nBBAND',
            style='yahoo',volume=True,savefig=dict(fname='tsave200.jpg',dpi=100,pad_inches=0.25))

    axes[0].legend(['upper','middle','lower'])
    fig.savefig('bband.png')