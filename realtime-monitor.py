import sys
from datetime import datetime, date, timedelta
import time
import requests
import yfinance as yf
import pandas as pd
import talib

def check_time():
    h = int(datetime.now().strftime("%H"))
    m = int(datetime.now().strftime("%M"))
    if (9<=h and h<=12) or (h==13 and m<=30):
    # if (0<=h and h<=24):
        return True
    else:
        return False

def get_realtime_info(sid):
    url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_"+sid+".tw"
    try:
        res = requests.get(url, headers={'content-type':'application/json'})
        # res = requests.get(url).json()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Get exception of realtime data.")
        return "-"
    res = res.json() 
    record = res['msgArray'][0]
    # print(record)
    return record

def check(sid,df,signal):
    stock_info = get_realtime_info(sid)
    if stock_info == '-':
        return False  
    # check price 
    price = stock_info['z']
    up_limit = stock_info['u']
    down_limit = stock_info['w']
    if price != '-':
        price = float(price)
        df['Close'][-1] = price
        df['ma'] = talib.SMA(df['Close'], timeperiod=20)
        print(str(datetime.now())+" "+str(price))
        if price > df['Close'][-2] * 1.05:           
            signal[0][0]=1
            print(signal[1][0])
        elif price < df['Close'][-2] * 0.95:
            signal[0][1]=1
            print(signal[1][1])
        if price >= float(up_limit) and signal[0][4] == 0:
            signal[0][4]=1
            print(signal[1][4])
        elif price <= float(down_limit) and signal[0][5] == 0:
            signal[0][5]=1
            print(signal[1][5])
        elif price > df['ma'][-1]:
            signal[0][7]=1
            print(signal[1][7])
        # check lots of hand on limit up.    
        last_volum = stock_info['tv']
        if last_volum != '-':
            last_volum = int(last_volum)
            if last_volum >=200 and signal[0][4] == 1 and signal[0][6] == 0:
                signal[0][6]=1
                print(signal[1][6])
    # check order volume
    five_self_vol = stock_info['f']
    five_self_vol = five_self_vol.split("_")
    five_self_price = stock_info['a']
    five_self_price = five_self_price.split("_")
    five_buy_vol = stock_info['g']
    five_buy_vol = five_buy_vol.split("_")
    five_buy_price = stock_info['b']
    five_buy_price = five_buy_price.split("_")
    if five_self_vol[0] != '-':
        for i in range(5):
            # if  int(five_self_vol[i]) >= 600 and signal[0][2] == 0:
            if  int(five_self_vol[i]) >= 600 :
                signal[0][2]=1
                print(signal[1][2].format(float(five_self_price[i]),int(five_self_vol[i])))
    if five_buy_vol[0] != '-':
        for i in range(5):
            # if int(five_buy_vol[i]) >= 600 and signal[0][3] == 0:
            if int(five_buy_vol[i]) >= 600 :
                signal[0][3]=1
                print(signal[1][3].format(float(five_buy_price[i]),int(five_buy_vol[i])))

def data_preprocess():
    today = date.today().strftime("%Y-%m-%d")
    start = date.today() - timedelta(days=30)
    # yf.pdr_override()
    df = yf.download(sid+'.TW', start, today)
    df = pd.DataFrame(data = df)
    df.loc[str(today)] = [0, 0, 0, 0, 0, 0]
    return df

if __name__ == "__main__":
    sid=sys.argv[1]
    stock_info = get_realtime_info(sid)
    while stock_info == '-':
        stock_info = get_realtime_info(sid)
        

    stock_name = stock_info['nf']

    print("Start to monitor "+sid+":"+stock_name+" in realtime.")
    print("--------------------------------------------------------------")
    print("- Price change +-5%")
    print("- Volume of sale/buy order exceed 600.")
    print("- Limit up/down.")
    print("- Lots of hands off on limit up")
    print("- Current price is higher than 20-day sma.")
    print("--------------------------------------------------------------")
    signal = [[0]*8,["[SIGNAL] Current price is UP to +5% of yesterday's closing price.",
    "[SIGNAL] Current price is DOWN to -5% of yesterday's closing price.",
    "[SIGNAL] Large orders of sell, Price:{} Volume:{}",
    "[SIGNAL] Large orders of buy, Price:{} Volume:{}",
    "[SIGNAL] Today's price is limit up!",
    "[SIGNAL] Today's price is limit down!",
    "[SIGNAL] Lots of hands off on limit up!",
    "[SIGNAL] Current price is higher than 20-day sma."
    ]]

    df = data_preprocess()
    # print(df)
    print(df.iloc[[-2]])
    while True:
        try:
            if not check_time():
                sys.exit("Non-trading time")
            check(sid,df,signal)
            time.sleep(5)
        except:
           print("Unexpected error:", sys.exc_info()[0])
