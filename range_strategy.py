import sys
import sys,datetime,numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mdates
import yfinance as yf
import talib

# Read argv from command
sid = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]
# Get data from yfinance to dataframe
yf.pdr_override()
df = yf.download(sid+'.TW', start, end)
df = pd.DataFrame(data = df)
order = pd.DataFrame(data=df['Close'])
orderTime = []
order['Close'].values[:] = np.nan
sell = pd.DataFrame(data=df['Close'])
sellTime = []
sell['Close'].values[:] = np.nan
profit=pd.DataFrame(data=df['Close'])
profit['Close'].values[:] = np.nan
order_sell_index=0
# 定義區間、停損停利點
box_ratio = 0.02
stoploss_ratio = 0.015
takeprofit_ratio = 0.07

# 定義績效
TotalProfit=0
StartPrice = df['Close'][0]
# 進場判斷
Index=0
for i in range(1,len(df.index)):
    price = df['Close'][i]
    if Index==0 :
        # 當價格突破上界
        if price >= StartPrice * (1+box_ratio):
            Index=1
            order.loc[df.index[i],'Close'] = df['Close'][i]
            orderTime.append(df.index[i])
            # 制定停損停利點
            StopLossPoint=StartPrice * (1-stoploss_ratio)
            TakeProfitPoint=StartPrice * (1+takeprofit_ratio)
        # 當價格突破下界
        elif price <= StartPrice * (1-box_ratio):
            Index=-1
            order.loc[df.index[i],'Close'] = df['Close'][i]
            orderTime.append(df.index[i])
            # 制定停損停利點
            StopLossPoint=StartPrice * (1+stoploss_ratio)
            TakeProfitPoint=StartPrice * (1-takeprofit_ratio)
    # 出場判斷
    if Index==1:
        # 停損判斷, 停利判斷, 最後強制出場
        if (price <= StopLossPoint) or (price >= TakeProfitPoint)or (i==len(df.index)-1):
            sell.loc[df.index[i], 'Close'] = df['Close'][i]
            sellTime.append(df.index[i])
            StartPrice = price
            Index=0
            Profit=sell.loc[sellTime[order_sell_index],'Close']-order.loc[orderTime[order_sell_index],'Close']
            TotalProfit+=Profit
            profit.loc[df.index[i], 'Close'] = TotalProfit
            print(sid,'Buy OrderTime',orderTime[order_sell_index],'OrderPrice',order.loc[orderTime[order_sell_index],'Close'],'CoverTime',sellTime[order_sell_index],'CoverPrice',sell.loc[sellTime[order_sell_index],'Close'],'Profit',Profit)
            order_sell_index+=1
    elif Index==-1:
        # 停損判斷, 停利判斷, 最後強制出場
        if (price >= StopLossPoint) or (price <= TakeProfitPoint)or (i==len(df.index)-1):
            sell.loc[df.index[i], 'Close'] = df['Close'][i]
            sellTime.append(df.index[i])
            StartPrice = price
            Index=0
            Profit=sell.loc[sellTime[order_sell_index],'Close']-order.loc[orderTime[order_sell_index],'Close']
            TotalProfit+=Profit
            profit.loc[df.index[i], 'Close'] = TotalProfit
            print(sid,'Buy OrderTime',orderTime[order_sell_index],'OrderPrice',order.loc[orderTime[order_sell_index],'Close'],'CoverTime',sellTime[order_sell_index],'CoverPrice',sell.loc[sellTime[order_sell_index],'Close'],'Profit',Profit)
            order_sell_index+=1

# plot strategy 
apds = [mpf.make_addplot(df['Close'],color='b'),
        mpf.make_addplot(order['Close'],type='scatter',markersize=200,marker='^'),
        mpf.make_addplot(sell['Close'],type='scatter',markersize=200,marker='v')
    ]
fig, axes=mpf.plot(df,type='candle',addplot=apds,returnfig=True,figscale=1.5,figratio=(16,9),title='\nRange strategy',
        style='yahoo',volume=True,volume_panel=1)
axes[0].legend(['Close price'])
fig.savefig('range_strategy.png')
    
# plot profit
profit=profit.dropna()
profit=profit.rename(columns={"Close": "Profit"})
profit.plot(kind='line',y='Profit', color='red')
plt.savefig('range_strategy_profit.png')

#顯示總績效
print('Total Profit',TotalProfit)





