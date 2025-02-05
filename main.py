# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

from pymongo import MongoClient
# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['wowple_db']




webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
# ChromeDriver 실행

# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities

# - 주소  입력
browser.get("https://play.google.com/store/apps/details?id=kr.co.cobosys.wowple&hl=ko-KR")

# - 가능 여부에 대한 OK 받음
pass

# - 정보 획득
from selenium.webdriver.common.by import By

time.sleep(2)
# 모달 화면 띄우기
selector_element = '#yDmH0d > c-wiz.SSPGKf.Czez9d > div > div > div:nth-child(1) > div > div.wkMJlb.YWi3ub > div > div.qZmL0 > div:nth-child(1) > c-wiz:nth-child(5) > section > div > div.Jwxk6d > div:nth-child(5) > div > div > button > span'

browser.find_element(by=By.CSS_SELECTOR, value=selector_element).click()

time.sleep(2)


# 정보 획득
selector_element = 'div.fysCi.Vk3ZVd'
element_scrollableDiv = browser.find_element(by=By.CSS_SELECTOR, value=selector_element)

# 스크롤 부분
previous_scrollHeight = 0
same_height_count = 0  # 같은 높이가 연속된 횟수를 카운트

while True:
    # JavaScript로 스크롤 실행
    browser.execute_script("arguments[0].scrollTo(arguments[1], arguments[0].scrollHeight)",
                         element_scrollableDiv, previous_scrollHeight)
    
    # 현재 스크롤 높이 가져오기
    current_scrollHeight = browser.execute_script("return arguments[0].scrollHeight",
                                               element_scrollableDiv)
    
    if previous_scrollHeight >= current_scrollHeight:
        same_height_count += 1
        if same_height_count >= 2:  # 두 번 연속으로 같은 높이가 나오면 종료
            break
    else:
        same_height_count = 0  # 높이가 변하면 카운터 리셋
        
    previous_scrollHeight = current_scrollHeight
    time.sleep(1)

# 마지막으로 한 번 더 스크롤
browser.execute_script("arguments[0].scrollTo(arguments[1], arguments[0].scrollHeight)",
                     element_scrollableDiv, current_scrollHeight)
time.sleep(1)



# 댓글 개수 확인 : div.RHo1pe
selector_element = '#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.HQdjr.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div > div > div > div.fysCi.Vk3ZVd > div > div:nth-child(2) > div'
element_comment = browser.find_elements(by=By.CSS_SELECTOR, value=selector_element)

print('count comment after done scroll : {}'.format(len(element_comment)))



review_elements = browser.find_elements(By.CSS_SELECTOR, "#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.HQdjr.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div > div > div > div.fysCi.Vk3ZVd > div > div:nth-child(2) > div")

for review in review_elements:
    try:
        writer = review.find_element(By.CSS_SELECTOR, "header > div.YNR7H > div.gSGphe > div").text
    except:
        writer = ''

    try:
        rate_element = review.find_element(By.CSS_SELECTOR, "header > div.Jx4nYe > div")
        aria_label = rate_element.get_attribute("aria-label")
        rate = int(aria_label.split('에 ')[1].split('개를')[0])
    except:
        rate = ''
    
    try:
        content = review.find_element(By.CSS_SELECTOR, "div.h3YV2d").text
    except:
        content = ''
    try:
        date = review.find_element(By.CSS_SELECTOR, "header > div.Jx4nYe > span").text
    except:
        date = ''
    
    try:
        suefull = review.find_element(By.CSS_SELECTOR, "div:nth-child(3) > div").text
        usefull = int(suefull.split('사용자 ')[1].split('명이')[0])
    except:
        usefull = 0

    # MongoDB에 바로 저장
    review_data = {
        'writer': writer,
        'content': content,
        'suefull': usefull,
        'date': date,
        'rating': rate
    }
    
    db.reviews.insert_one(review_data)


pass


# browser.save_screenshot('./formats.png')
# 브라우저 종료
browser.quit()