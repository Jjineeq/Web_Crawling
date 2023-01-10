import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# 카테고리를 이름과 코드명으로 딕셔너리로 만들고 코드명 21개로 월봉 차트 값 구하는 for문 돌리고 내보내기

category_dic = {'음식료품' : 'D0011005', '섬유의복' : 'D0011006', '종이목재' : 'D0011007'}
#, '화학' : , '의약품' : , '비금속광물' : , '철강금속' : , '기계' : ,
#        '전기전자' : , '의료정밀' : , '운수장비' : , '유통업' : , '전기가스업' : , '건설업' : , '운수창고' : , '통신업' : , '금융업' : ,
#        '은행' : , '증권' : , '보험' : , '서비스업' : }

category = ['음식료품', '섬유의복', '종이목재', '화학', '의약품', '비금속광물', '철강금속', '기계',
       '전기전자', '의료정밀', '운수장비', '유통업', '전기가스업', '건설업', '운수창고', '통신업', '금융업',
       '은행', '증권', '보험', '서비스업']

def category_stock():
    #url = 'https://finance.daum.net/api/charts/D0011024/months?limit=200&adjusted=true'
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

    for i in range(0,2):
        url_k = url + category_dic[category[i]] + '/months?limit=200&adjusted=true'
        print(url_k)
        headers['referer'] = headers['referer'] + category_dic[category[i]]
        r = requests.get(url_k, headers=headers, params=params)
        szContent = r.text
        #print (szContent)

        #soup = BeautifulSoup(html, 'html.parser')
        #titles = soup.select('span')

        str_list = []
        list = json.loads(szContent)
        # print(list)
        for price in list["data"]:
            str_list.append(price["date"] + " : " + str(price["tradePrice"]))
            # print(str_list) 
        str_list = pd.DataFrame(str_list)
        result = pd.concat([result, str_list], axis=1)
    print(result)

category_stock()
