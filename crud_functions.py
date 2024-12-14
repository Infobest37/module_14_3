import sqlite3

conn = sqlite3.connect('database.db')

def initiate_db():
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users_2(
    id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    emale TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL);""")
    conn.commit()
def add_user(user_name, emale, age):
    cursor = conn.cursor()
    check_user = cursor.execute("SELECT * FROM Users_2 WHERE user_name = ?", (user_name, ))
    if check_user.fetchone() is None:
        cursor.execute("INSERT INTO Users_2 (user_name, emale, age, balance) VALUES (?, ?, ?, ?)",
                                     (user_name,emale, age,1000))# При добавлении нового пользователя его баланс
                                                                             # составляет 1000
        conn.commit()


def is_included(user_name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users_2 WHERE user_name = ?", (user_name,))
    return cursor.fetchone() is not None


