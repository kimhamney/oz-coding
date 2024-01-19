from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
from main.models import Product
import pymysql

bp = Blueprint('main', __name__, url_prefix='/')

def load_products():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='1111',
        db='kreamproducts',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    
    cursor = connection.cursor()

    sql = "SELECT * FROM products"
    cursor.execute(sql)

    datas = cursor.fetchall()
    products = []
    for data in datas:
        product = Product(data)
        products.append(product)

    return products

@bp.route('/')
def index():
    products = load_products()

    return render_template('index.html', products=products)