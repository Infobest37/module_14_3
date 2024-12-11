import sqlite3
conn = sqlite3.connect('database2.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
id INT,
title TEXT,
description TEXT,
price INT);""")


for i in range(1,5):
    cursor.execute("INSERT INTO Users VALUES (?, ?, ?, ?)",
        (f"{i}", f"Product{i}", f"Описание{i}", f"{i*100}"))
def get_all_products():
    connection = sqlite3.connect('database2')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    return products




conn.commit()
conn.close()