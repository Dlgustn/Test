from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import ContentParsing  # ContentParsing.py 파일에서 정의한 모듈을 import

def main(Content):
    
      # 원하는 정보 추출

      if Content == '임금조건':
            value = ContentParsing.ContentParse(Content, '임금조건')
      
      elif Content == '신청기간':
            value = ContentParsing.ContentParse(Content, '신청기간')
      
      elif Content == '사업명':
            value = ContentParsing.ContentParse(Content, '사업명')
      
      elif Content == '근무지':
            value = ContentParsing.ContentParse(Content, '근무지')
      
      elif Content == '등록일':
            value = ContentParsing.ContentParse(Content, '등록일')
      
      elif Content == '문의처':
            value = ContentParsing.ContentParse(Content, '문의처')


main()
