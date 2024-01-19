from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
from main.models import Product
import sqlite3
import os.path

bp = Blueprint('main', __name__, url_prefix='/')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../../data/products.db")
connection = sqlite3.connect(db_path, check_same_thread=False)

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