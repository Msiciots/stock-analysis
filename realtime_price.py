import requests
import json  
import pandas as pd
import time
from datetime import datetime

url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_2330.tw"
data = {'time':[],
        'code':[],
        'price':[],
        'av':[],
        'v':[]
        }
while True:
    h = int(datetime.now().strftime("%H"))
    m = int(datetime.now().strftime("%M"))
    if (9<=h and h<=12) or (h==13 and m<=30):
        for i in range(20):
            res = requests.get(url).json()
            record = res['msgArray'][0]
            t = record['d'] + "-" + record['t']
            data['time'].append(t)
            data['code'].append(record['c'])
            data['price'].append(record['z'])
            data['v'].append(record['v'])
            data['av'].append(record['av'])
            time.sleep(5)
            if i==19:
                df = pd.DataFrame(data=data)
                df.to_csv("data.csv", index = False)
                # df = df.set_index('time')
    else:
        continue
