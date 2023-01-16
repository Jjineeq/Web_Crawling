import requests 
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import json
import time




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
    
def news_function(category, start, end, page, header):
    """
    input은 4개입니다.
    카테고리는 '검색 이름'
    start는 시작날짜 : '20221101' -> 22년 11월 01일 부터 검색
    end는 종료날짜 : '20221203' -> 22년 12월 03일 까지 검색
    page는 몇개의 페이지를 저장할건지 : 3 -> 3페이지
    header는 크롬에서 F12 누르고 Network -> All -> Headers -> User-Agent 복사해서 dict형태로 넣어주면 됩니다.

    ex) 
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    news_function('음식료품','20221101','20221203',3, header) 
    -> 음식료품을 검색해서 22년 11월 1일부터 22년 12월 3일까지 3페이지씩 저장한다.

    개인에 맞게 변경해야되는 것은 to_csv 주소입니다. 이것은 개인 컴퓨터에 맞게 변경해야됩니다.
    """

    query = category
    header = header 
    
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



def category_stock():
    """
    카테고리별로 2012-12-28일부터 현재까지 달의 마지막날 종가 지수를 가져옴.

    """
    
    category_dic = {'음식료품' : 'D0011005', '섬유의복' : 'D0011006', '종이목재' : 'D0011007', '화학' : 'D0011008', '의약품' : 'D0011009', '비금속광물' : 'D0011010', '철강금속' : 'D0011011', '기계' : 'D0011012',
                '전기전자' : 'D0011013', '의료정밀' : 'D0011014', '운수장비' : 'D0011015', '유통업' : 'D0011016', '전기가스업' : 'D0011017', '건설업' : 'D0011018', '운수창고' : 'D0011019', '통신업' : 'D0011020', '금융업' : 'D0011021',
                '은행' : 'D0011022', '증권' : 'D0011024', '보험' : 'D0011025', '서비스업' : 'D0011026'}
    category = ['음식료품', '섬유의복', '종이목재', '화학', '의약품', '비금속광물', '철강금속', '기계', '전기전자', '의료정밀', '운수장비', 
                '유통업', '전기가스업', '건설업', '운수창고', '통신업', '금융업', '은행', '증권', '보험', '서비스업']

    url = 'https://finance.daum.net/api/charts/'
    headers = {
        "referer": "https://finance.daum.net/domestic/sectors/",
        "user-agent": "Mozilla/5.0"
    }

    params = {
        "limit": "200",
        "adjusted": "true"
    }

    result = pd.DataFrame()

    for i in range(0,21):
        url_k = url + category_dic[category[i]] + '/months?limit=200&adjusted=true'  # 카테고리별 월봉 차트의 url
        headers['referer'] = headers['referer'] + category_dic[category[i]]
        r = requests.get(url_k, headers=headers, params=params)
        szContent = r.text

        str_list = []
        list = json.loads(szContent)
        for price in list["data"]: # 월봉 차트에 있는 모든 주가를 가져온다.
            str_list.append(price["date"] + " : " + str(price["tradePrice"]).replace(".0", "")) 
        str_list = pd.DataFrame(str_list)
        result = pd.concat([result, str_list], axis=1)
    result.columns = ['음식료품', '섬유의복', '종이목재', '화학', '의약품', '비금속광물', '철강금속', '기계', '전기전자', '의료정밀', '운수장비', 
                '유통업', '전기가스업', '건설업', '운수창고', '통신업', '금융업', '은행', '증권', '보험', '서비스업']
    return result


def last_day_of_month(any_day):
    """
    해당월에 마지막 날짜를 구하는 함수입니다.
    """
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


def weight_cal(news_score, weights):
    """ 
    news_score는 news 긍부정 분석으로 나온 positive count/(positive count + negative count) 값입니다.

    news_score는 list형태로 input, weights는 dict형태로 input을 받아야 합니다.
    
    최종 리턴값은 seires형태로 finish weight으로 나갑니다.
    """
    result = []
    for i in range(len(news_score)):
        news_score_i = news_score[i]
        weights_i = weights[i]
        
        if (news_score_i >= 0.6) & (weights_i >= 0.1) & (weights_i < 0.2) : # news가 매우 긍정, 포트폴리오는 보통 가중치
            total_weight = news_score_i*0.2 + weights_i
        
        if (news_score_i >= 0.6) & (weights_i >= 0.2) : # news가 매우 긍정, 포트폴리오도 강한 가중치
            total_weight = news_score_i*0.25 + weights_i
        
        if (news_score_i >= 0.55) & (weights_i >= 0.1) & (weights_i <0.2) : # news가 매우 긍정, 포트폴리오는 약한 가중치
            total_weight = news_score_i * 0.15 + weights_i
        
        # if (news_score_i >= 0.55) & (weights_i >= 0.1) : # news가 긍정, 포트폴리오는 보통 가중치
        #     total_weight = news_score_i * 0.2 + weights_i * 0.8
        
        
        if (news_score_i <= 0.45) & (weights_i >= 0.2) : # news가 부정, 포트폴리오는 강한 가중치
            total_weight = weights_i - news_score_i*0.1
        
        if (news_score_i <= 0.45) & (weights_i <= 0.1) : # news가 부정, 포트폴리오는 약한 가중치
            total_weight = weights_i - news_score_i*0.2
        
        if (news_score_i <= 0.4) & (weights_i <= 0.1) :  # news가 매우 부정, 포트폴리오는 약한 가중치
            total_weight = 0
        
        if total_weight <= 0 :
            total_weight = 0
        
        result.append(total_weight)
    result = pd.Series(result)
    finish__weight = result/result.sum()
    return finish__weight         

