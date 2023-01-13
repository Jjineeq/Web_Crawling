import requests 
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm




category = ['음식료품', '섬유의복', '종이목재', '화학', '의약품', '비금속광물', '철강금속', '기계',
       '전기전자', '의료정밀', '운수장비', '유통업', '전기가스업', '건설업', '운수창고', '통신업', '금융업',
       '은행', '증권', '보험', '서비스업']

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def flatten(lst):
    result = []
    for item in lst:
        if type(item) == list:
            result += flatten(item)
        else:
            result += [item]
    return result
    
def news_function(category, start, end, page):
    """
    input은 4개입니다.
    카테고리는 '검색 이름'
    start는 시작날짜 : '20221101' -> 22년 11월 01일 부터 검색
    end는 종료날짜 : '20221203' -> 22년 12월 03일 까지 검색
    page는 몇개의 페이지를 저장할건지 : 3 -> 3페이지

    ex) news_function('음식료품','20221101','20221203',3) 
    -> 음식료품을 검색해서 22년 11월 1일부터 22년 12월 3일까지 3페이지씩 저장한다.

    개인에 맞게 변경해야되는 것은 header, to_csv 주소입니다.
    """

    query = category
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'} 
    
    date = pd.date_range(start,end)
    
    news_all = []
    news_title = []
    page = np.arange(page)
    for i in tqdm(date):
        date = str(i).replace('-','')[0:8]
        for j in list(page):
            page_2 = (j - 1)*10 +10
            url = 'https://search.naver.com/search.naver?where=news&query={}&sort=3&nso=so%3Ar%2Cp%3Afrom{}to{}&start={}'.format(query, date, date, page_2)
            res = requests.get(url, headers = header)
            #time.sleep(1.5) # 학교 기준 1.5초 집에서는 0초 가능
            soup = bs(res.text, 'lxml')
            for title in soup.find_all('a', attrs={'class':'news_tit'}):
                news_title.append([date, title['title']])
    news_title = pd.DataFrame(news_title).drop_duplicates()
    news_title['category'] = query
    news_title.columns = ['time','title','category']
    news_title.to_csv('C:/Users/user/github/Web_Crawling/save_data/'+ query +'_total.csv',encoding='utf-8-sig', index=False) # csv 내보내기
    return news_title