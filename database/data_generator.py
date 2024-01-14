import mysql.connector
from faker import Faker
import random

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="testdatabase"
)

cursor = db_connection.cursor()
faker = Faker()

for _ in range(100):
    username = faker.user_name()
    email = faker.email()

    sql = "INSERT INTO users(username, email) VALUES(%s, %s)"
    values = (username, email)
    cursor.execute(sql, values)

cursor.execute("SELECT user_id FROM users")
valud_user_id = [row[0] for row in cursor.fetchall()]

for _ in range(100):
    user_id = random.choice(valud_user_id)
    product_name = faker.word()
    quantity = random.randint(1, 10)

    try:
        sql = "INSERT INTO orders(user_id, product_name, quantity) VALUES(%s, %s, %s)"
        values = (user_id, product_name, quantity)
        cursor.execute(sql, values)
    except Exception as e:
        print(e)
        pass

db_connection.commit()
cursor.close()
db_connection.close()