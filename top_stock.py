import yfinance as yf
from bs4 import BeautifulSoup
import requests

def top_stock(top_rank,start,end):
    page = BeautifulSoup(requests.get('https://www.taifex.com.tw/cht/9/futuresQADetail').text, "html.parser")
    soup = page.find_all('td',{'headers':'name_a'})
    company_rank=[x.text.strip() for x in soup]
    sids=[]
    for i in range(0,top_rank*2,2):
        sids.append(company_rank[i])

    print(sids)

    yf.pdr_override()
    dfs=[]
    for sid in sids:
        dfs.append(yf.download(sid+'.TW', start, end))
    return dfs

