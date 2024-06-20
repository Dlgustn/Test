from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Chrome 옵션 설정
options = Options()
options.add_argument("--start-maximized")  # 브라우저 창을 최대화된 상태로 시작

# ChromeDriver 경로 설정 및 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 네이버 지도 웹사이트로 이동
driver.get('https://map.naver.com')

# 페이지 로드 대기
time.sleep(5)

# 프레임로 전환하기 위해 충분한 대기 시간 확보
time.sleep(5)

# 프레임 전환 시도
try:
    # 프레임을 이름 또는 ID로 찾기
    driver.switch_to.frame("searchIframe")
except Exception as e:
    print(f"An error occurred while switching to the iframe: {e}")
    # 프레임을 찾지 못한 경우, 다른 방법 시도
    try:
        # 프레임을 CSS 선택자로 찾기
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[name="searchIframe"]')
        driver.switch_to.frame(iframe)
    except Exception as e:
        print(f"An error occurred while switching to the iframe using CSS selector: {e}")

# iframe 내에서 작업 수행 예시
try:
    # 검색 입력 필드 찾기
    search_box = driver.find_element(By.CSS_SELECTOR, "input#search-input")
    # 검색어 입력
    search_box.send_keys("Seoul", Keys.ENTER)
except Exception as e:
    print(f"An error occurred while performing actions within the iframe: {e}")

# 사용자 입력 대기 (브라우저가 닫히지 않도록)
input("브라우저를 닫으려면 Enter 키를 누르세요...")

# 드라이버 종료
driver.quit()