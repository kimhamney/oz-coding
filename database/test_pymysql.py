import pymysql

connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='1111',
    db='classicmodels',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# SELECT * FROM
def get_customers():
    cursor = connection.cursor()

    sql = "SELECT * FROM customers"
    cursor.execute(sql)

    customers = cursor.fetchone()

    print(customers)

# INSERT INTO
def add_customer():
    cursor = connection.cursor()

    name = 'ham'
    f_name = 'kim'
    sql = f"INSERT INTO customers(customerNumber, customerName, contactLastName) VALUES({10000}, '{name}', '{f_name}')"
    cursor.execute(sql)
    connection.commit()

# UPDATE SET
def update_customer():
    cursor = connection.cursor()

    update_name = 'update_ham'
    update_lastname = 'update_kim'
    sql = f"UPDATE customers SET customerName='{update_name}', contactLastName='{update_lastname}' WHERE customerNumber=10000"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    
# DELETE FROM
def delete_customer():
    cursor = connection.cursor()
    sql = "DELETE FROM customers WHERE customerNumber=10000"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

delete_customer()