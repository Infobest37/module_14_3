from db14_3 import *
class ConnectionTables:
    def __init__(self, connection):
        self.connection = sqlite3.connect('database2.db')
        self.cursor = connection.cursor()


    def create_tables(self, product_id):
        self.connection = sqlite3.connect('database2.db')
        cursor = self.connection.cursor()
        cursor.execute("SELECT id ,title ,description, price FROM products WHERE id = ?", (product_id))
        return cursor.fetchall()

    def get_all_products(self):
        # Получение всех продуктов из таблицы
        self.connection = sqlite3.connect('database2.db')
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title, description, price FROM products")
        return cursor.fetchall()

product_table = ConnectionTables(sqlite3.connect('database2.db'))