import sys,datetime,numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mdates
import yfinance as yf
import talib

sid=sys.argv[1]
# Read argv from command
sid = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]

# Get data from yfinance to dataframe
yf.pdr_override()
df = yf.download(sid+'.TW', start, end)
df = pd.DataFrame(data = df)
print(df)
order = pd.DataFrame(data=df['Close'])
orderTime = []
order['Close'].values[:] = np.nan
sell = pd.DataFrame(data=df['Close'])
sellTime = []
sell['Close'].values[:] = np.nan
profit=pd.DataFrame(data=df['Close'])
profit['Close'].values[:] = np.nan
# 定義績效
TotalProfit=0
# 計算MA技術指標
sma_10 = talib.SMA(df['Close'], timeperiod=10)
# 計算RSI技術指標
rsi_10 = talib.RSI(df['Close'], timeperiod=10)
# 進場判斷
Index=0
order_sell_index=0
for i in range(10,len(df.index)):
    # 定義策略需要的變數 價格、上一筆價格、MA、上一筆MA、RSI
    price = df['Close'][i]
    lastprice = df['Close'][i-1]
    ma = sma_10[i]
    lastma = sma_10[i-1]
    rsi = rsi_10[i]
    # 進場判斷
    if Index==0:
        # 當 RSI > 50 並且價格向上突破MA 進場做多
        if rsi>50 and lastprice<=lastma and price>ma :
            Index=1
            order.loc[df.index[i],'Close'] = df['Close'][i]
            orderTime.append(df.index[i])

        # 當 RSI < 50 並且價格向下突破MA 進場做空
        elif rsi<50 and lastprice>=lastma and price<ma :
            Index=-1
            order.loc[df.index[i],'Close'] = df['Close'][i]
            orderTime.append(df.index[i])
    # 多單出場判斷
    elif Index==1:
        # 當價格向下突破MA 多單出場
        if lastprice>=lastma and price<ma:
            sell.loc[df.index[i], 'Close'] = df['Close'][i]
            sellTime.append(df.index[i])
            Index=0
            Profit=sell.loc[sellTime[order_sell_index],'Close']-order.loc[orderTime[order_sell_index],'Close']
            TotalProfit+=Profit
            profit.loc[df.index[i], 'Close'] = TotalProfit
            print(sid,'Buy OrderTime',orderTime[order_sell_index],'OrderPrice',order.loc[orderTime[order_sell_index],'Close'],'CoverTime',sellTime[order_sell_index],'CoverPrice',sell.loc[sellTime[order_sell_index],'Close'],'Profit',Profit)
            order_sell_index+=1
        # 最後強制出場
        elif i==len(df.index)-1:
            sell.loc[df.index[i], 'Close'] = df['Close'][i]
            sellTime.append(df.index[i])
            Profit=sell.loc[sellTime[order_sell_index],'Close']-order.loc[orderTime[order_sell_index],'Close']
            TotalProfit+=Profit
            profit.loc[df.index[i], 'Close'] = TotalProfit
            print(sid,'Buy OrderTime',orderTime[order_sell_index],'OrderPrice',order.loc[orderTime[order_sell_index],'Close'],'CoverTime',sellTime[order_sell_index],'CoverPrice',sell.loc[sellTime[order_sell_index],'Close'],'Profit',Profit)
            order_sell_index+=1
    # 空單出場判斷
    elif Index==-1:
        # 當價格向上突破MA 空單出場
        if lastprice<=lastma and price>ma:
            sell.loc[df.index[i], 'Close'] = df['Close'][i]
            sellTime.append(df.index[i])
            Index=0
            Profit=sell.loc[sellTime[order_sell_index],'Close']-order.loc[orderTime[order_sell_index],'Close']
            TotalProfit+=Profit
            profit.loc[df.index[i], 'Close'] = TotalProfit
            print(sid,'Buy OrderTime',orderTime[order_sell_index],'OrderPrice',order.loc[orderTime[order_sell_index],'Close'],'CoverTime',sellTime[order_sell_index],'CoverPrice',sell.loc[sellTime[order_sell_index],'Close'],'Profit',Profit)
            order_sell_index+=1
        # 最後強制出場
        elif i==len(df.index)-1:
            sell.loc[df.index[i], 'Close'] = df['Close'][i]
            sellTime.append(df.index[i])
            Profit=sell.loc[sellTime[order_sell_index],'Close']-order.loc[orderTime[order_sell_index],'Close']
            TotalProfit+=Profit
            profit.loc[df.index[i], 'Close'] = TotalProfit
            print(sid,'Buy OrderTime',orderTime[order_sell_index],'OrderPrice',order.loc[orderTime[order_sell_index],'Close'],'CoverTime',sellTime[order_sell_index],'CoverPrice',sell.loc[sellTime[order_sell_index],'Close'],'Profit',Profit)
            order_sell_index+=1
# plot strategy 
apds = [mpf.make_addplot(df['Close'],color='b'),
        mpf.make_addplot(sma_10,color='c'),
        mpf.make_addplot(order['Close'],type='scatter',markersize=200,marker='^'),
        mpf.make_addplot(sell['Close'],type='scatter',markersize=200,marker='v'),
        mpf.make_addplot(rsi_10,panel=1,color='fuchsia',secondary_y=True)
    ]
fig, axes=mpf.plot(df,type='candle',addplot=apds,returnfig=True,figscale=1.5,figratio=(16,9),title='\nMA_RSI strategy',
        style='yahoo',volume=True,volume_panel=2)
axes[0].legend(['Close price','sma_10'])
axes[3].legend(['rsi_10'])
fig.savefig('ma_rsi_strategy.png')
    
# plot profit
profit=profit.dropna()
profit=profit.rename(columns={"Close": "Profit"})
profit.plot(kind='line',y='Profit', color='red')

plt.savefig('ma_rsi_strategy_profit.png')

#顯示總績效
print('Total Profit',TotalProfit)
