import datetime
import pandas as pd
from stockstats import StockDataFrame
import matplotlib.pyplot as plt
import mplfinance as mpf

if __name__ == "__main__":
    # df = pd.read_csv('test.csv');
    df = pd.read_csv('STOCK_DAY_2330_202101.csv');
    print(df)
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='any')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
    df = df.set_index('Date')
    print(df)
    print (df.dtypes)
    # mpf.plot(df)
    # stock_df = df.rename(columns={'Closing Price': 'close', 
    #                             'Opening Price': 'open',
    #                             'Highest Price': 'high',
    #                             'Lowest Price': 'low',
    #                             'Trade Volume': 'volume',
    #                             'Transaction': 'amount'
    #                             })
    stock_df = df.rename(columns={'Closing Price': 'Close', 
                                'Opening Price': 'Open',
                                'Highest Price': 'High',
                                'Lowest Price': 'Low',
                                'Trade Volume': 'Volume',
                                'Transaction': 'Amount'
                                })
    stock_df = StockDataFrame.retype(stock_df)
    print (stock_df.dtypes)
    # mpf.plot(stock_df)
    
    # df['SMA_10'] = df['Closing Price'].rolling(10).mean()
    # df['EMA_12'] = df['Closing Price'].ewm(span=12).mean()
    # df['EMA_26'] = df['Closing Price'].ewm(span=26).mean()
    # stock_df['adx']
    # stock_df['macd']
    # stock_df['boll']
    
    # df1 = df[['SMA_10', 'EMA_12', 'EMA_26']]
    # df2 = stock_df[['adx', 'macd', 'boll']]
    # res = pd.concat([df1, df2], axis=1)
    # print(res)

    
