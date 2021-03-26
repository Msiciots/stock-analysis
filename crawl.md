# 爬取網頁資料
## 爬取各種面向排行榜
### 產業別股票清單
透過 [MoneyDJ 理財網](https://www.moneydj.com/) 來取得爬蟲資訊，每個分類都會有指定的代碼，在該網站中是透過「A」的變數名稱來進行值得定義。例如，車輛相關類的車燈
https://www.moneydj.com/z/zh/zha/ZH00.djhtm?A=C015105
### 本益比排行
利用[台灣證券交易所](https://www.twse.com.tw/zh/page/trading/exchange/BWIBBU_d.html)網站抓取股票資訊，再篩選出本益比資料。  
http://www.tse.com.tw/exchangeReport/BWIBBU_d?response=json&date=20181214&selectType=01  
date: 日期  
selectType: 股票分類種類
### 殖利率排行
同上
### 股價淨值比排行
同上
### 單日熱門股
利用雅虎上市熱門股排行網頁爬取資料  
https://tw.stock.yahoo.com/d/i/rank.php?t=&e=tse&n=50  
t 代表排行榜種類: vol, up, down, pdis, pri, amt  
e 代表上市(tse)或上櫃(otc)  
n 顯示的交易數量(30~100)  
### 買賣超排行榜
使用雅虎外資買賣超排行榜
#### 外資
單日買超:https://tw.stock.yahoo.com/d/i/fgbuy_tse.html  
上週買超:https://tw.stock.yahoo.com/d/i/fgbuy_tse_w.html  
單日賣超:https://tw.stock.yahoo.com/d/i/fgsell_tse.html  
上週賣超:https://tw.stock.yahoo.com/d/i/fgbuy_tse_w.html  
#### 自營商
單日買超:https://tw.stock.yahoo.com/d/i/sebuy_tse.html  
上週買超:https://tw.stock.yahoo.com/d/i/sebuy_tse_w.html  
單日賣超:https://tw.stock.yahoo.com/d/i/sesell_tse.html  
上週賣超:https://tw.stock.yahoo.com/d/i/sebuy_tse_w.html  