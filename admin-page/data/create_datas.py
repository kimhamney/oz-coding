from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3
import time
import re

def main():
    datas = get_datas()
    execute_db(datas)
    
def execute_db(datas):
    connection = sqlite3.connect('./products.db')

    create_table(connection)
    insert_datas(connection, datas)

def insert_datas(connection, datas):
    cursor = connection.cursor()
    
    for data in datas:
        for i in data:
            sql = f'''INSERT INTO products(name, category, price, url, image_url, review, sales) 
                      VALUES("{i['name']}", "{i['category']}", {i['price']}, "{i['url']}", "{i['image_url']}", {i['review']}, {i['sales']})
                  '''
            cursor.execute(sql)

    connection.commit()

def create_table(connection):
    cursor = connection.cursor()

    sql = ''' CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price INTEGER,
            url TEXT,
            image_url TEXT,
            review INTEGER,
            sales INTEGER
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