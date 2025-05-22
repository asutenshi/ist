import sqlite3
import hashlib
from datetime import datetime


class DBManager:
    def __init__(self, db_name="base.db"):
        self.db_name = db_name
        self._init_tables()

    def _init_tables(self):
        from tables import create_tables
        create_tables(self.db_name)

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def _hash_password(self, password):
        """Создает хэш пароля для безопасного хранения"""
        return hashlib.sha256(password.encode()).hexdigest()

    # ===== Методы для работы с пользователями =====
    def register_user(self, login, password, name, surname, address):
        """Регистрация нового пользователя"""
        conn = self._connect()
        cursor = conn.cursor()
        try:
            # Создаем запись в таблице customers
            cursor.execute(
                "INSERT INTO customers (name, surname, address) VALUES (?, ?, ?)",
                (name, surname, address)
            )
            customer_id = cursor.lastrowid

            # Создаем запись в таблице users
            hashed_password = self._hash_password(password)
            cursor.execute(
                "INSERT INTO users (login, password, customer_id) VALUES (?, ?, ?)",
                (login, hashed_password, customer_id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Ошибка при дублировании логина
            conn.rollback()
            return False
        finally:
            conn.close()

    def login_user(self, login, password):
        """Авторизация пользователя"""
        conn = self._connect()
        cursor = conn.cursor()
        hashed_password = self._hash_password(password)

        cursor.execute(
            "SELECT * FROM users WHERE login = ? AND password = ?",
            (login, hashed_password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            return dict(user)
        return None

    def get_user_details(self, user_id):
        """Получить детальную информацию о пользователе"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT u.id, u.login, u.is_admin, c.name, c.surname, c.address
            FROM users u
            JOIN customers c ON u.customer_id = c.id
            WHERE u.id = ?
            """,
            (user_id,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None

    # ===== Методы для работы с категориями =====
    def get_all_categories(self):
        """Получить список всех категорий"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return categories

    def add_category(self, name):
        """Добавить новую категорию"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        
    def update_category(self, category_id, name):
        """Обновить данные категории"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (name, category_id))
        conn.commit()
        conn.close()
        
    def delete_category(self, category_id):
        """Удалить категорию"""
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Нельзя удалить категорию, если на неё ссылаются товары
            conn.rollback()
            return False
        finally:
            conn.close()

    # ===== Методы для работы с компаниями =====
    def get_all_companies(self):
        """Получить список всех компаний"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companies")
        companies = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return companies
        
    def add_company(self, name, state):
        """Добавить новую компанию"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO companies (name, state) VALUES (?, ?)", (name, state))
        conn.commit()
        conn.close()
        
    def update_company(self, company_id, name, state):
        """Обновить данные компании"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE companies SET name = ?, state = ? WHERE id = ?", 
                      (name, state, company_id))
        conn.commit()
        conn.close()
        
    def delete_company(self, company_id):
        """Удалить компанию"""
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM companies WHERE id = ?", (company_id,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Нельзя удалить компанию, если на неё ссылаются товары
            conn.rollback()
            return False
        finally:
            conn.close()

    # ===== Методы для работы с товарами =====
    def get_products_by_category(self, category_id):
        """Получить список товаров по категории"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.*, c.name as category_name, com.name as company_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN companies com ON p.company_id = com.id
            WHERE p.category_id = ?
            """,
            (category_id,)
        )
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return products
    
    def get_all_products(self):
        """Получить список всех товаров"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.*, c.name as category_name, com.name as company_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN companies com ON p.company_id = com.id
            """
        )
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return products
        
    def add_product(self, name, category_id, company_id, price, quantity):
        """Добавить новый товар"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, category_id, company_id, price, total_quantity)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, category_id, company_id, price, quantity)
        )
        conn.commit()
        conn.close()
        
    def update_product(self, product_id, name, category_id, company_id, price, quantity):
        """Обновить данные товара"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE products
            SET name = ?, category_id = ?, company_id = ?, price = ?, total_quantity = ?
            WHERE id = ?
            """,
            (name, category_id, company_id, price, quantity, product_id)
        )
        conn.commit()
        conn.close()
        
    def delete_product(self, product_id):
        """Удалить товар"""
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_product(self, product_id):
        """Получить информацию о товаре по id"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.*, c.name as category_name, com.name as company_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN companies com ON p.company_id = com.id
            WHERE p.id = ?
            """,
            (product_id,)
        )
        product = cursor.fetchone()
        conn.close()
        
        if product:
            return dict(product)
        return None

    # ===== Методы для работы с корзиной =====
    def add_to_cart(self, user_id, product_id, quantity):
        """Добавить товар в корзину"""
        conn = self._connect()
        cursor = conn.cursor()
        
        # Проверяем, есть ли товар в наличии
        cursor.execute("SELECT total_quantity FROM products WHERE id = ?", (product_id,))
        available = cursor.fetchone()
        
        if not available or available['total_quantity'] < quantity:
            conn.close()
            return False
        
        # Проверяем, есть ли уже этот товар в корзине
        cursor.execute(
            "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        existing = cursor.fetchone()
        
        if existing:
            # Обновляем количество
            new_quantity = existing['quantity'] + quantity
            cursor.execute(
                "UPDATE cart SET quantity = ? WHERE id = ?",
                (new_quantity, existing['id'])
            )
        else:
            # Добавляем новую запись
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                (user_id, product_id, quantity)
            )
            
        conn.commit()
        conn.close()
        return True
    
    def update_cart_item(self, cart_id, quantity):
        """Обновить количество товара в корзине"""
        conn = self._connect()
        cursor = conn.cursor()
        
        # Получаем информацию о товаре в корзине
        cursor.execute(
            "SELECT c.*, p.total_quantity FROM cart c JOIN products p ON c.product_id = p.id WHERE c.id = ?",
            (cart_id,)
        )
        item = cursor.fetchone()
        
        if not item or item['total_quantity'] < quantity:
            conn.close()
            return False
        
        cursor.execute("UPDATE cart SET quantity = ? WHERE id = ?", (quantity, cart_id))
        conn.commit()
        conn.close()
        return True
    
    def remove_from_cart(self, cart_id):
        """Удалить товар из корзины"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
        conn.commit()
        conn.close()
    
    def get_cart(self, user_id):
        """Получить содержимое корзины пользователя"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.id, c.quantity, p.id as product_id, p.name, p.price, 
                  (c.quantity * p.price) as total_price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
            """,
            (user_id,)
        )
        cart_items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return cart_items
    
    def get_cart_total(self, user_id):
        """Получить общую стоимость корзины"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT SUM(c.quantity * p.price) as total
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
            """,
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result and result['total']:
            return result['total']
        return 0

    def clear_cart(self, user_id):
        """Очистить корзину пользователя"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

    # ===== Методы для оформления покупки =====
    def checkout(self, user_id, pup_id):
        """Оформить покупку"""
        conn = self._connect()
        cursor = conn.cursor()
        
        try:
            # Получаем данные о пользователе
            cursor.execute("SELECT customer_id FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            if not user:
                conn.close()
                return None
                
            customer_id = user['customer_id']
            
            # Получаем содержимое корзины
            cart_items = self.get_cart(user_id)
            if not cart_items:
                conn.close()
                return None
                
            # Проверяем наличие товаров
            for item in cart_items:
                cursor.execute(
                    "SELECT total_quantity FROM products WHERE id = ?",
                    (item['product_id'],)
                )
                product = cursor.fetchone()
                
                if not product or product['total_quantity'] < item['quantity']:
                    conn.close()
                    return None
            
            # Создаем чек
            total_price = self.get_cart_total(user_id)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                """
                INSERT INTO cheques (sale_date, customer_id, total_price, pup_id)
                VALUES (?, ?, ?, ?)
                """,
                (current_date, customer_id, total_price, pup_id)
            )
            
            sale_id = cursor.lastrowid
            
            # Создаем записи о продаже товаров
            for item in cart_items:
                cursor.execute(
                    """
                    INSERT INTO movements (sale_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                    """,
                    (sale_id, item['product_id'], item['quantity'], item['price'])
                )
                
                # Уменьшаем количество товаров
                cursor.execute(
                    """
                    UPDATE products
                    SET total_quantity = total_quantity - ?
                    WHERE id = ?
                    """,
                    (item['quantity'], item['product_id'])
                )
            
            # Очищаем корзину
            cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
            
            conn.commit()
            return sale_id
            
        except Exception as e:
            conn.rollback()
            return None
        finally:
            conn.close()

    # ===== Методы для работы с чеками =====
    def get_user_cheques(self, user_id):
        """Получить список чеков пользователя"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT ch.*, p.address as pickup_address
            FROM cheques ch
            JOIN users u ON ch.customer_id = u.customer_id
            JOIN pups p ON ch.pup_id = p.id
            WHERE u.id = ?
            ORDER BY ch.sale_date DESC
            """,
            (user_id,)
        )
        
        cheques = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return cheques
    
    def get_cheque_details(self, cheque_id):
        """Получить детали чека"""
        conn = self._connect()
        cursor = conn.cursor()
        
        # Получаем основную информацию о чеке
        cursor.execute(
            """
            SELECT ch.*, c.name, c.surname, c.address, p.address as pickup_address
            FROM cheques ch
            JOIN customers c ON ch.customer_id = c.id
            JOIN pups p ON ch.pup_id = p.id
            WHERE ch.id = ?
            """,
            (cheque_id,)
        )
        
        cheque = cursor.fetchone()
        if not cheque:
            conn.close()
            return None
            
        cheque_dict = dict(cheque)
        
        # Получаем товары из чека
        cursor.execute(
            """
            SELECT m.quantity, m.price, p.name
            FROM movements m
            JOIN products p ON m.product_id = p.id
            WHERE m.sale_id = ?
            """,
            (cheque_id,)
        )
        
        items = [dict(row) for row in cursor.fetchall()]
        cheque_dict['items'] = items
        
        conn.close()
        return cheque_dict

    # ===== Методы для работы с пунктами выдачи =====
    def get_all_pups(self):
        """Получить список всех пунктов выдачи"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pups")
        pups = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return pups
        
    def add_pup(self, address):
        """Добавить новый пункт выдачи"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pups (address) VALUES (?)", (address,))
        conn.commit()
        conn.close()
        
    def update_pup(self, pup_id, address):
        """Обновить данные пункта выдачи"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE pups SET address = ? WHERE id = ?", (address, pup_id))
        conn.commit()
        conn.close()
        
    def delete_pup(self, pup_id):
        """Удалить пункт выдачи"""
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM pups WHERE id = ?", (pup_id,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            conn.rollback()
            return False
        finally:
            conn.close()