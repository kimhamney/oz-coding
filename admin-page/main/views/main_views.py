from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
from main.models import Product
import pymysql

bp = Blueprint('main', __name__, url_prefix='/')

connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='1111',
    db='kreamproducts',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

def load_products():
    cursor = connection.cursor()

    sql = "SELECT * FROM products"
    cursor.execute(sql)

    datas = cursor.fetchall()
    products = []
    for data in datas:
        product = Product(data)
        products.append(product)

    return products

def load_category(category):
    cursor = connection.cursor()

    sql = f"SELECT * FROM products WHERE category='{category}'"
    cursor.execute(sql)

    datas = cursor.fetchall()
    products = []
    for data in datas:
        product = Product(data)
        products.append(product)

    return products

def search_products(search):
    cursor = connection.cursor()

    sql = f"SELECT * FROM products WHERE name LIKE '%{search}%'"
    cursor.execute(sql)

    datas = cursor.fetchall()
    products = []
    for data in datas:
        product = Product(data)
        products.append(product)

    return products

@bp.route('/')
def main():
    products = load_products()
    return render_template('index.html', products=products)

@bp.route('/category/', methods=('GET', 'POST'))
def category():
    category = request.args.get('category', type=str, default='')
    products = load_category(category)
    return render_template('index.html', products=products, category=category)

@bp.route('/search/', methods=('GET', 'POST'))
def search():
    search = request.args.get('search', type=str, default='')
    products = search_products(search)
    return render_template('index.html', products=products)