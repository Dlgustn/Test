from datetime import date
import requests # html 요청 보내기 위한 라이브러리
from bs4 import BeautifulSoup # html 파싱하기 위한 라이브러리 뷰티플수프
from os import path # 환경변수를 위한 라이브러리(파일 경로)
import time # 아이오토의 슬립 커맨드랑 유사한 기능을 쓰기위한 라이브러리
from urllib.parse import quote # url에 한글부분 변환을 위한 라이브러리
import pandas as Pd # 엑셀 데이터를 다루기 위한 판다스 라이브러리
import socket

# 아이오토에서 쓰려면 함수나 클래스 형태여야 함
def Temp():
    # 엑셀 파일 경로 할당
    UserName = path.expanduser('~')
    FileName = path.join(UserName, "Desktop", "PythonTest.xlsx")  
    # username이 환경변수 이고 Desktop = 바탕화면 PythonTest.xlsx = 파일이름

    # 엑셀 파일 판다스로 데이터프레임 형태로 읽어오기
    Df = Pd.read_excel(FileName, sheet_name='Sheet2')

    # url에서 html 받아오는 함수 retries = 재시도 회수 backoff_factor = 재시도 대기 시간
    def GetPageContent(url, retries=3, backoff_factor=1.0):
        
        #헤더는 로봇이 아닌 일반 유저가 여는 것처럼 보이기 위함 > 로봇은 밴하는 사이트들이 종종 있음
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        for i in range(retries):#리퀘스트 보내기 포문인 이유는 재시도 > 아이오토와 비슷하다 보면 됨
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8' # utf-8로 인코딩
                return response.text
            
            elif response.status_code == 429: #가장 자주 본 오류
                print(f"투 매니 리퀘스트 오류 {backoff_factor} 후 제시도")
                time.sleep(backoff_factor)
                backoff_factor *= 2

            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
                break
        return None

    # 도로명 주소를 업데이트할 리스트와 삭제할 행 인덱스 리스트
    UpdateList = []
    DeleteIndices = []

    # 네이버 지도 url > 검색 전
    url = "https://pcmap.place.naver.com/mart/list?query="
    
    # 회사명을 검색한 결과화면 html 받아와서 도로명 주소 추출
    for i in range(len(Df)): # 데이터 프레임 길이 만큼 수행
        print(Df.at[i, '도로명 주소'])
        # 회사명이 있고, 도로명 주소가 없는 경우 -- 가장 일반적이고 정상적인 경우
        if Pd.isna(Df.at[i, '도로명 주소']) and not Pd.isna(Df.at[i, '회사명']):
            
            CompanyName = Df.at[i, '회사명'] #회사명 할당
            EncodedCompanyName = quote(CompanyName) # 회사명 인코딩
            CompanyUrl = url + EncodedCompanyName # 회사명 검색 결과 화면 url 할당

            HtmlContent = GetPageContent(CompanyUrl) # html 할당(html 받아오는 함수)

            # html 잘 받아왔으면 파싱해서 도로명 주소 찾고 도로명주소를 리스트에 모아두기
            if HtmlContent:

                Soup = BeautifulSoup(HtmlContent, 'lxml') # 뷰티플 수프로 파싱
                SpanElements = Soup.find_all('span', class_='Pb4bU') # 도로명 주소 태그, 클래스로 찾기

                if SpanElements: # 도로명 주소 있으면 
                    FirstSpanText = SpanElements[0].get_text() # 가장 첫번째 결과 gettext
                    UpdateList.append((i, FirstSpanText)) # 리스트에 담기
                
                else: # 도로명 주소 없으면
                    print(f"Element not found for {CompanyName}") # 로그
                    UpdateList.append((i, "검색 결과가 없습니다.")) # 검색결과 없음 리스트에 담기

            else: # html이 없으면 로그
                print(f"Failed to retrieve the webpage after retries for {CompanyName}")
        
        # 회사명이 없고 도로명 주소가 있는 경우 삭제 리스트에 추가
        elif Pd.isna(Df.at[i, '회사명']) and not Pd.isna(Df.at[i, '도로명 주소']):
            
            DeleteIndices.append(i)
        

    #print(delete_indices)
    #print(update_list)

    # 도로명 주소 업데이트
    for idx, road_name in UpdateList:
        Df.at[idx, '도로명 주소'] = road_name

    print(Df)

    # 삭제할 행을 제거
    Df.drop(index=DeleteIndices, inplace=True)

    # NAN 값 제거
    dffin = Df.dropna()
    print(dffin)
    
    # 엑셀 파일 저장
    dffin.to_excel(FileName, sheet_name='Sheet2', index=False)

    TempList = {'허종운': '1', '이현수' : '2', '장형렬' : '3'}
    return(TempList)

    #데이터프레임 html로 전환해서 웹으로 띄우기
    HtmlTable = dffin.to_html(index=False, classes='table table-striped')
    with open('dataframe.html', 'w', encoding='utf-8') as f:
        f.write(HtmlTable)

    

    
Temp()
