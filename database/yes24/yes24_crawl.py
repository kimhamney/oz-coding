from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql
import re
from datetime import datetime

ChromeDriverManager().install()

browser = webdriver.Chrome()

link_list = []
for i in range(1, 4):
    url = f'https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber={i}&pageSize=24'

    browser.get(url)
    datas = browser.find_elements(By.CLASS_NAME, 'gd_name')

    for i in datas:
        link = i.get_attribute('href')
        link_list.append(link)
        print(link)

    time.sleep(3)



conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1111',
    db='yes24',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    for link in link_list:
        browser.get(link)

        title = browser.find_element(By.CLASS_NAME, 'gd_name').text
        author = browser.find_element(By.CLASS_NAME, 'gd_auth').text
        publisher = browser.find_element(By.CLASS_NAME, 'gd_pub').text
        publishing = browser.find_element(By.CLASS_NAME, 'gd_date').text

        match = re.search(r'(\d+)년 (\d+)월 (\d+)일', publishing)
        if match:
            year, month, day = match.groups()
            date_obj = datetime(int(year), int(month), int(day))
            publishing = date_obj.strftime("%Y-%m-%d")
        else:
            publishing = "2024-01-01"

        rating = browser.find_element(By.CLASS_NAME, 'yes_b').text

        review = browser.find_element(By.CLASS_NAME, 'txC_blue').text
        review = int(review.replace(",", ""))

        sales = browser.find_element(By.CLASS_NAME, 'gd_sellNum').text.split(" ")[2]
        sales = int(sales.replace(",", ""))
        
        price = browser.find_element(By.CLASS_NAME, 'yes_m').text[:-1]
        price = int(price.replace(",", ""))

        full_text = browser.find_element(By.CLASS_NAME, 'gd_best').text
        parts = full_text.split(" | ")

        if len(parts) == 1:
            ranking = 0
            ranking_weeks = 0
        else:
            try:
                ranking_part = parts[0]
                ranking = ''.join(filter(str.isdigit, ranking_part))
            except:
                ranking = 0

            try:
                ranking_weeks_part = parts[1]
                ranking_weeks = ''.join(filter(str.isdigit, ranking_weeks_part.split()[-1]))
            except:
                ranking_weeks = 0

        sql = """INSERT INTO Books(
            title, author, publisher, publishing, rating, review, sales, price, ranking, ranking_weeks)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(sql, (title, author, publisher, publishing, rating, review, sales, price, ranking, ranking_weeks))
        conn.commit()

        time.sleep(2)