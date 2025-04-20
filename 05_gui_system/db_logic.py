# %%
import sqlite3
from datetime import datetime

# %%
class DatabaseManager:
    def __init__(self, db_path='database/baza.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def close(self):
        if self.connection:
            self.connection.commit() 
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def get_categories(self):
        self.cursor.execute("""
            SELECT id, category
            FROM categories
            ORDER BY category
        """)
        return self.cursor.fetchall()
    
    def get_products(self):
        self.cursor.execute("""
            SELECT p.id, c.category, p.name, price, quantity
            FROM products p
            JOIN categories c ON p.id_category = c.id
            ORDER BY c.category
        """)
        return self.cursor.fetchall()
    
    def get_goods(self, date):
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Дата должна быть в формате 'YYYY-MM-DD'")

        if not isinstance(date, datetime):
            raise TypeError("date должен быть объектом datetime или строкой в формате 'YYYY-MM-DD'")
        
        date_str = date.strftime('%Y-%m-%d')

        self.cursor.execute("""
            SELECT p.name, SUM(h.quantity)
            FROM history h
            JOIN receipts r ON h.id_receipt = r.id
            JOIN products p ON h.id_product = p.id
            WHERE DATE(r.date) = ?
            GROUP BY h.id_product
        """, (date_str,))
        return self.cursor.fetchall()

    def get_solds(self, date):
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Дата должна быть в формате 'YYYY-MM-DD'")

        if not isinstance(date, datetime):
            raise TypeError("date должен быть объектом datetime или строкой в формате 'YYYY-MM-DD'")
        
        date_str = date.strftime('%Y-%m-%d')

        self.cursor.execute("""
            SELECT SUM(r.total_price)
            FROM receipts r
            WHERE DATE(r.date) = ?
            GROUP BY DATE(r.date)
        """, (date_str,))
        return self.cursor.fetchall()
    
    def buy_products(self, products, date, total_price):
        # prod : (id_prod, quantity, price)
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError("Дата должна быть в формате 'YYYY-MM-DD HH:MM:SS'")

        if not isinstance(date, datetime):
            raise TypeError("date должен быть объектом datetime или строкой в формате 'YYYY-MM-DD HH:MM:SS'")

        date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    
        try:
            for product in products:
                id_prod, quantity, price = product
                
                self.cursor.execute("""
                    SELECT quantity
                    FROM products
                    WHERE id = ?
                """, (id_prod, ))

                available = self.cursor.fetchone()
                if available is None:
                    raise Exception(f"Товар с ID {id_prod} не найден")
                
                if available[0] < quantity:
                    raise Exception(f"Недостотачно товара с ID {id_prod}. Доступно: {available}, запрощено: {quantity}")

            self.cursor.execute("""
                INSERT INTO receipts (date, total_price)
                VALUES (?, ?)
            """, (date_str, total_price))

            receipt_id = self.cursor.lastrowid

            for product in products:
                id_prod, quantity, price = product

                self.cursor.execute("""
                    INSERT INTO history (id_receipt, id_product, quantity, price)
                    VALUES (?, ?, ?, ?)
                """, (receipt_id, id_prod, quantity, price))

                self.cursor.execute("""
                    UPDATE products
                    SET quantity = quantity - ?
                    WHERE id = ?
                """, (quantity, id_prod))

                self.connection.commit()
            return receipt_id            

        except sqlite3.Error as e:
            self.connection.rollback()
            raise Exception(f'Ошибка при создании чека: {e}')