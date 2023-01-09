import csv
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By
import pandas as pd
import requests

browser = webdriver.Chrome()
#browser.maximize_window() # 창 최대화


# url 정의 - 네이버 뉴스 경제란
url_finance = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=259&sid1=101&date='
url_stock = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=258&sid1=101&date='

# 경제 page 이동


page = [1,2,3,4,5]

date = pd.date_range('2015-01-01','2015-01-05')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
result_finance = []

for i in date:
    date = str(i).replace('-','')[0:8]
    url = url_finance + date
    for k in page:
        url_q = url+'&page='+'{}'.format(k)
        url_k = browser.get(url_q)
        time.sleep(0.5)
        print(url_q)
        response = requests.get(url_q, headers=headers)
        html_text = response.text
        soup = bs(html_text,'html.parser')
        link = list(soup.select('li>dl>dt>a'))
        for j in link:
            href = j.text.replace('\n','').replace('\t','').replace(' ','')
            result_finance.append(href)
