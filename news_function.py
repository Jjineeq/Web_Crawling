import csv
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By
from tqdm import tqdm

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def finace(start, end, page):
    """
    example : 
    finace('2020-01-01', '2022-01-01', 1) 
    -> 2020년 1월 1일부터 2022년 1월 1일까지 경제뉴스 금융 탭 뉴스 제목을 1페이지씩 저장
    
    start : 시작일
    end : 종료일
    page : 페이지 수
    
    """
    #크롬창 열기
    browser = webdriver.Chrome()
    #browser.maximize_window() # 창 최대화

    # 호스트 연결 끊기는것 방지
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url_finance = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=259&sid1=101&date='
    date = pd.date_range(start, end)
    page = np.arange(page)
    result_finance = [] # 저장할 빈 리스트
    for i in date:
        date = str(i).replace('-','')[0:8]
        url = url_finance + date
        for k in page:
            url_q = url+'&page='+'{}'.format(k)
            url_k = browser.get(url_q)
            time.sleep(0.5)
            #print(url_q)
            response = requests.get(url_q, headers=headers)
            html_text = response.text
            soup = bs(html_text,'html.parser')
            link = list(soup.select('li>dl>dt>a'))
            for j in link:
                href = j.text.replace('\n','').replace('\t','').replace(' ','')
                result_finance.append([date,href])
                
        
    sol = pd.DataFrame(result_finance)
    sol.columns = ['date','title']
    fiance_result = sol[sol.title != '']
    
    return fiance_result


def stock(start, end, page):
    """
    example : 
    stock('2020-01-01', '2022-01-01', 1) 
    -> 2020년 1월 1일부터 2022년 1월 1일까지 경제뉴스 증권 탭 뉴스 제목을 1페이지씩 저장
    
    start : 시작일
    end : 종료일
    page : 페이지 수
    
    매월 마지막일 기준으로 년-월.csv 으로 저장
    to_csv('링크 수정 필요합니다')
       
    """
    check = []
    
    if (start[0:4]==end[0:4]):
        year = int(start[0:4])
        for month in range(1, 13):
                check.append((str(last_day_of_month(datetime.date(year, month, 1)))))
    else:
        for year in range(int(start[0:4]),int(end[0:4])+1):
            for month in range(1, 13):
                check.append((str(last_day_of_month(datetime.date(year, month, 1)))))
                
    browser = webdriver.Chrome()
        #browser.maximize_window() # 창 최대화

        # 호스트 연결 끊기는것 방지
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url_stock = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=258&sid1=101&date='
    date = pd.date_range(start, end)
    page = np.arange(page)
    result_stock = []
    for i in tqdm(date):
        date = str(i).replace('-','')[0:8]
        url = url_stock + date
        for k in page:
            url_q = url+'&page='+'{}'.format(k)
            url_k = browser.get(url_q)
            time.sleep(1.5)
            response = requests.get(url_q, headers=headers)
            html_text = response.text
            soup = bs(html_text,'html.parser')
            link = list(soup.select('li>dl>dt>a'))
            for j in link:
                href = j.text.replace('\n','').replace('\t','').replace(' ','')
                result_stock.append([date,href])
        print(i)
        if str(i)[0:10] in check:
            sol = pd.DataFrame(result_stock)
            sol.columns = ['date','title']
            stock_result = sol[sol.title != '']
            stock_result = stock_result[stock_result.title !='동영상기사'].drop_duplicates(['title'])
            stock_result.to_csv('C:/Users/user/github/Web_Crawling/save_data/'+'{}'.format(str(i)[0:7]+'.csv'),encoding='utf-8-sig', index=False)
            result_stock = []
            stock_result = []
        else:
            pass
        
    return stock_result
                
#finace('2020-01-01', '2022-01-01', 1)
#stock('2020-01-01', '2022-01-01', 1)