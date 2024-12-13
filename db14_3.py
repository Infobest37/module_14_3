import sqlite3
from aiogram.types import Message

conn = sqlite3.connect('database2.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Products(
id INT,
title TEXT,
description TEXT,
price INT);""")


# for i in range(1,5):
#     cursor.execute("INSERT INTO Products VALUES (?, ?, ?, ?)",
#         (f"{i}", f"Product{i}", f"Описание{i}", f"{i*100}"))

# cursor.execute("DELETE FROM Products WHERE id ")
def get_all_products():
      # Получение всех продуктов из таблицы
      connection = sqlite3.connect('database2.db')
      cursor = connection.cursor()
      cursor.execute("SELECT title, description, price FROM Products")
      return cursor.fetchall()
products = get_all_products()

for i in products:
   print(i)










conn.commit()
conn.close()