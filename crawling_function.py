from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys
import getpass

driver = webdriver.Chrome(path)

def title_search(url, date, page):
    url = url + date + '&page=' + str(page)
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 1. 기사제목
    title_list = []  # 기사제목
    for i in soup.find('div',{'class':'list_body newsflash_body'}).find_all('a'):
        title_text = i.get_text(strip=True)
        #title_text = title_text.strip('\n''\t'' ') # \n, \t, 공백 문자열 제거
        #title_text = title_text.replace(' ','')
        #title_text = title_text.replace(',','')	# , 문자 제거
        #title_text = title_text.replace('"','')	# " 문자 제거
        title_list.append(title_text)
    title_list = list(filter(None, title_list)) # 빈 리스트 삭제

    # 2. href
    href_list = []  # href
    # href 주소
    for i in soup.find('div',{'class':'list_body newsflash_body'}).find_all('li'):
        href_list.append([i.find('a')['href']])


    # 딕셔너리
    data_dic = dict(zip(title_list, href_list))

    return data_dic

def content_search(url):
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    content_list = []
    for i in soup.find('div',{'id':'articleBodyContents'}):
        content_text = i.get_text()
        content_text = content_text.strip('\n''\t'' ') # \n, \t 문자열 제거
        content_text = content_text.replace('\'','"')
        #content_text = content_text.replace(' ','')
        content_list.append(content_text)
    #content_list = [i.strip('\n') for i in content_list[:]]
    content_list = list(filter(None, content_list))
    content_list.remove(content_list[0])

    content = ''
    for i in content_list:
        content = content + ' ' + i

    return content