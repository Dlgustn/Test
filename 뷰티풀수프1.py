import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from lxml import etree
import os

url = "https://pcmap.place.naver.com/mart/list?query="
companyname = "하이마트"
companyurl = url + companyname


#1 웹 키고 가져오기

# WebDriver 인스턴스 생성
driver = webdriver.Chrome()

# 웹 페이지 불러오기
driver.get(companyurl)

# 페이지 소스 가져오기
page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

tree = etree.HTML(str(soup))
element = tree.xpath('//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/div/div/div/span[2]/a/span[1]')

for item in element:
    print(item.text)


driver.quit