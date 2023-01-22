import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화
#browser.set_window_size(400,600)

category = ['음식료품', '섬유의복', '종이목재', '화학', '의약품', '비금속광물', '철강금속', '기계',
       '전기전자', '의료정밀', '운수장비', '유통업', '전기가스업', '건설업', '운수창고', '통신업', '금융업',
       '은행', '증권', '보험', '서비스업']

# 1. 페이지 이동
url = 'https://finance.daum.net/domestic/sectors'
browser.get(url)
time.sleep(1)

result = []

# 2. 업종으로 이동
for i in range(0,21): 
    click1 = browser.find_element(By.LINK_TEXT, category[i])
    click1.click()
    time.sleep(1)

    # 3. 업종, 날짜, 주가 데이터 확보
    name = browser.find_element(By.XPATH, '//*[@id="labTitle"]').text
    price = browser.find_element(By.XPATH, '//*[@id="boxDashboard"]/div/div/span[1]/strong').text
    day = browser.find_element(By.XPATH, '//*[@id="boxMarketStatus"]').text
    name = name[0:len(category[i])]
    day = day[0:5]
    if i == 0:
        price = float(price.replace(',',""))
        result.append(name)
        result.append(price)
        result.append(day)
        result = pd.DataFrame(result)
    else:
        add = []
        price = float(price.replace(',',""))
        add.append(name)
        add.append(price)
        add.append(day)
        add = pd.DataFrame(add)
        result = pd.concat([result, add], axis=1)
    browser.back() # 뒤로가기    
    time.sleep(1)

# 브라우저 종료
browser.quit()
print(result)