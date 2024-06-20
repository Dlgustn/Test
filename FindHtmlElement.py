import requests
import time
from bs4 import BeautifulSoup

def GetPageContent(url, Tagname, Attribute, retries=3, backoff_factor=1.0):        

        #헤더는 로봇이 아닌 일반 유저가 여는 것처럼 보이기 위함 > 로봇은 밴하는 사이트들이 종종 있음
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        #HtmlContent = ""
        UpdateList = []

        for i in range(retries):#리퀘스트 보내기 포문인 이유는 재시도 > 아이오토와 비슷하다 보면 됨
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8' # utf-8로 인코딩
                
                HtmlContent = response.text

                Soup = BeautifulSoup(HtmlContent, 'lxml') # 뷰티플 수프로 파싱
                SpanElements = Soup.find_all('span', class_='Pb4bU') # 도로명 주소 태그, 클래스로 찾기

                if SpanElements: # 도로명 주소 있으면 
                    FirstSpanText = SpanElements[0].get_text() # 가장 첫번째 결과 gettext
                    UpdateList.append((i, FirstSpanText)) # 리스트에 담기
                
                else: # 도로명 주소 없으면
                    print(f"찾는 요소가 없습니다.") # 로그
                    UpdateList.append((i, "")) # 검색결과 없음 리스트에 담기

                print (UpdateList)
                return UpdateList

            elif response.status_code == 429: #가장 자주 본 오류
                print(f"투 매니 리퀘스트 오류 {backoff_factor} 후 제시도")
                time.sleep(backoff_factor)
                backoff_factor *= 2

            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
                break
        return None


                