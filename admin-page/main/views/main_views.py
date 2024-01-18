from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
import pymysql

bp = Blueprint('main', __name__, url_prefix='/')

def load_datas():
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

    return datas

@bp.route('/')
def index():
    datas = load_datas()
    return render_template('index.html')