import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
id INT,
username TEXT,
first_name TEXT,
block INT);""")

def adduser(id, username, first_name):
    check_user = cursor.execute("SELECT * FROM Users WHERE id = ?", (id,))
    if check_user.fetchone() is None:
        cursor.execute(f'''INSERT INTO Users VALUES ('{id}', '{username}', '{first_name}',0,)''')
        conn.commit()


conn.commit()
conn.close()