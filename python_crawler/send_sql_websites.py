import mysql.connector
from mysql.connector import Error
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

f = open(os.path.join(__location__, 'data.txt'), "r", encoding="utf-8")

lines = f.read().split("\n")

f.close()

def create_connection(host_name, user_name, user_password, data):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=data
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("HOST_NAME", "USER_NAME", "USER_PASSWORD", "DATABASE_NAME")

cursor = connection.cursor()

sql = "INSERT INTO websites (url, title, keywords) VALUES (%s, %s, %s)"
val = []

for l in lines:
    items = l.split("#")
    if len(items) == 3:
        entry = (items[0].replace("#", ""), items[1].replace("#", ""), items[2].replace("#", ""))
        val.append(entry)

print("executing...")
cursor.executemany(sql, val)

print("commiting...")

try:
    connection.commit()
except:
    print("Cannot commit!")


cursor.close()
connection.close()