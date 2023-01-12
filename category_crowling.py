import requests 
import lxml
from bs4 import BeautifulSoup as bs
from datetime import datetime
import csv
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time
import re

category = ['음식료품', '섬유의복', '종이목재', '화학', '의약품', '비금속광물', '철강금속', '기계',
       '전기전자', '의료정밀', '운수장비', '유통업', '전기가스업', '건설업', '운수창고', '통신업', '금융업',
       '은행', '증권', '보험', '서비스업']

result = []
query = str(category[13])
ds = '2020.01.01'
de = '2020.01.31'
page = '1' # 페이지당 10씩 증가 (page-1)*10+1


ds_from =  ds.replace(".","")
de_to = ds.replace(".","")
header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"} 
cookie = {'CONSENT' : 'YES'}

#url = 'https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={}&de={}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20200101to20200131&is_sug_officeid=0&start={}'.format(query, ds, de, page)
url = 'https://search.naver.com/search.naver?where=news&query={}&sort=3&ds={}&de={}&nso=so%3Ar%2Cp%3Afrom{}to{}&start={}'.format(query, ds, de, ds_from, de_to, page)
#url = 'https://search.naver.com/search.naver?where=news&query=건설업&sort=3&ds=2020.01.01&de=2020.01.31&nso=so%3Ar%2Cp%3Afrom20200101to20200131&start=1'
res = requests.get(url, headers = header)
soup = bs(res.text, 'lxml')

# 기사 제목
news_title = [title['title'] for title in soup.find_all('a', attrs={'class':'news_tit'})] 
# 기사 날짜들(list)
dates = [ date.get_text() for date in soup.find_all('span', attrs={'class':'info'})]
# 기사 날짜들에서 년, 월 뽑기
date = []
year = []
month = []
for i in dates:
    date.append(i[:10])
    year.append(i[:4])
    month.append(i[5:7])

for j in date:
    dates = j.replace('.','-')

result_1 = result.append([dates, year, month, news_title, query])
print(result_1)
result = pd.DataFrame(result_1)
print(result)