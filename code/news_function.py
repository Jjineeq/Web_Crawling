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
                
    #크롬창 열기
    browser = webdriver.Chrome()
    #browser.maximize_window() # 창 최대화

    # 호스트 연결 끊기는것 방지
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url_finance = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=259&sid1=101&date='
    date = pd.date_range(start, end) # 시작일부터 종료일까지 생성
    page = np.arange(page) # 입력페이지 맞춰 범위 설정
    result_finance = [] # 저장할 빈 리스트

    for i in tqdm(date):
        date = str(i).replace('-','')[0:8] # 날짜 문자열로 변경후 ex)20220110 처럼 변경
        url = url_finance + date # 주소 설정
        for k in page: # 페이지변경
            url_q = url+'&page='+'{}'.format(k) # 주소설정
            url_k = browser.get(url_q) 
            time.sleep(1.5) # 호스트가 강제로 끊으면 랜덤하게 변경
            #print(url_q)
            response = requests.get(url_q, headers=headers) # 값 받아오기
            html_text = response.text # text만 남기기
            soup = bs(html_text,'html.parser') # 문서 파싱
            link = list(soup.select('li>dl>dt>a')) # li dl dt a 순서로 내려옴
            for j in link:
                href = j.text.replace('\n','').replace('\t','').replace(' ','') # 가져온 text 처리하게 쉽게 replace
                result_finance.append([date,href])  # 빈 리스트에 추가
        print(i) # 날짜 확인용
        if str(i)[0:10] in check: # 말일이랑 같은지 확인하고 해당월 마지막일이면 csv 내보내기 
            sol = pd.DataFrame(result_finance) # 리스트 df로 변경
            sol.columns = ['date','title'] # columns 변경
            finace_result = sol[sol.title != ''] # 빈 값 제거
            finace_result = finace_result[finace_result.title !='동영상기사'].drop_duplicates(['title']) # 의미 없는 내용 제거
            finace_result = finace_result[finace_result.title !='[표]']
            finace_result.to_csv('C:/Users/user/github/Web_Crawling/save_data/'+'{}'.format(str(i)[0:7]+'_finance.csv'),encoding='utf-8-sig', index=False) # csv 내보내기
            result_finance = [] # 다시 빈 리스트로
            finace_result = [] #다시 빈 리스트로
        else: # 말일 아니면 패스
            pass
        
    return finace_result


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
            stock_result = stock_result[stock_result.title !='표']
            stock_result.to_csv('C:/Users/user/github/Web_Crawling/save_data/'+'{}'.format(str(i)[0:7]+'_stock.csv'),encoding='utf-8-sig', index=False)
            result_stock = []
            stock_result = []
        else:
            pass
        
    return stock_result
                
#finace('2020-01-01', '2022-01-01', 1)
#stock('2020-01-01', '2022-01-01', 1)