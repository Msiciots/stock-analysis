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
        return True
    else:
        return False
def get_realtime_price(sid):
    url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_"+sid+".tw"
    res = requests.get(url).json()
    record = res['msgArray'][0]
    return record['z']
def check_entry(sid,df):
    if get_realtime_price(sid) == "-":
        return False
    price = float(get_realtime_price(sid))
    if price > df['ma'][-1]:
        return price
    else:
        return False
def check_exit(sid,df):
    if get_realtime_price(sid) == "-":
        return False
    price = float(get_realtime_price(sid))
    if price < df['ma'][-1]:
        return price
    else:
        return False
def data_preprocess():
    today = date.today().strftime("%Y-%m-%d")
    start = date.today() - timedelta(days=30)
    yf.pdr_override()
    df = yf.download(sid+'.TW', start, today)
    df = pd.DataFrame(data = df)
    df['ma'] = talib.SMA(df['Close'], timeperiod=10)
    return df
if __name__ == "__main__":
    sid=sys.argv[1]

    if not check_time():
        sys.exit("Non-trading time")  

    isInMarket = False 
    df = data_preprocess()
    while True:
        if isInMarket:
            price = check_exit(sid,df)
            if price:
                isInMarket = False
                print("[Signal] Exit, Current price is lower than MA")
                print("Price:"+price+" MA:"+df['MA'][-1])
        else:
            price = check_entry(sid,df)
            if price:
                isInMarket = True
                print("[Signal] Entry, Current price is higher than MA.")
                print("Price:"+price+" MA:"+df['MA'][-1])
        time.sleep(5)
        
