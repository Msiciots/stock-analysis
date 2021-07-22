import requests 
from bs4 import BeautifulSoup

def get_stock_name(sid):
    url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2" 
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    response = requests.get(url,headers=headers) 
    html_doc = response.text # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser") # 指定 lxml 作為解析器

    cols = soup.find_all('td', attrs={'bgcolor':'#FAFAD2'})
    # print(cols)

    # rows = table_body.find_all('tr')
    col_count = 1
    for col in cols:
        if col.text==" 上市認購(售)權證  ":
            break
        if col_count==0:
            t = col.text.split()
            id = t[0]
            name = t[1]
            if id == sid:
                return name
            
            col_count = 7
        col_count -= 1
        # input("Please enter your name: ")

    return "Stock not found."

