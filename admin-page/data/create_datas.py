from bs4 import BeautifulSoup
from selenium import webdriver

#셀레니움에 다양한 옵션을 적용시키기 위한 패키지
from selenium.webdriver.chrome.options import Options

#크롬 드라이버 매니저를 실행시키기 위해 설치해주는 패키지
from selenium.webdriver.chrome.service import Service
#자동으로 크롬 드라이브를 최신으로 유지해주는 패키지 
from webdriver_manager.chrome import ChromeDriverManager
#클래스, 아이디, css_selector를 이용하고자 할때
from selenium.webdriver.common.by import By
#키보드 입력
from selenium.webdriver.common.keys import Keys

import pymysql

import time
import re

def main():
    datas = get_datas()
    execute_db(datas)
    
def execute_db(datas):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='1111',
        db='kreamproducts',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    create_table(connection)
    insert_datas(connection, datas)

def insert_datas(connection, datas):
    cursor = connection.cursor()
    
    for data in datas:
        for i in data:
            sql = '''INSERT INTO products(name, category, price, url, image_url, review, sales) 
                      VALUES(%s, %s, %s, %s, %s, %s, %s)
                '''
            cursor.execute(sql, (i['name'], i['category'], i['price'], i['url'], i['image_url'], i['review'], i['sales']))

    connection.commit()

def create_table(connection):
    cursor = connection.cursor()

    sql = ''' CREATE TABLE products (
            id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(255),
            price INT,
            url VARCHAR(255),
            image_url VARCHAR(255),
            review INT,
            sales INT
          )
          '''
    cursor.execute(sql)
    connection.commit()

def get_datas():
    user = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    options_ = Options()
    options_.add_argument(f"User-Agent={user}")
    options_.add_experimental_option("detach", True)
    options_.add_experimental_option("excludeSwitches", ["enable-logging"])

    #크롬 드라이버 매니저를 자동으로 설치되도록 실행시키는 코드
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options_)

    url = "https://kream.co.kr/search?keyword=Nike&tab=products&shop_category_id="

    datas = []
    categories = {"아우터":"63", "신발":"34", "상의":"64", "하의":"65", "가방":"9", "패션잡화":"7"}
    for key, value in categories.items():
        driver.get(url + value)
        time.sleep(0.5)

        crawling_datas = crawling_products(driver, key)
        datas.append(crawling_datas)

    return datas

def crawling_products(driver, category):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    items = soup.select(".product_card")

    product_list = []
    for i in items:
        name = i.select_one(".translated_name").text
        url = "https://kream.co.kr" + i.select_one(".item_inner").attrs["href"]
        image_url = i.select_one(".product_img>img").attrs["src"]
        review = get_digits(i.select_one(".review_figure").text)
        price = get_digits(i.select_one(".amount").text)
        sales = i.select_one(".status_value").text
        sales = get_digits(sales) * 10000 if "만" in sales else get_digits(sales)

        item = {"category":category, 
                "name":name, 
                "price":price, 
                "url":url, 
                "image_url":image_url, 
                "review":review, 
                "sales":sales}
        
        product_list.append(item)

    return product_list

def get_digits(text):
    if text == '':
        return 0
    return int(re.sub(r'[^0-9]', '', text))
    
if __name__== "__main__":
    main()