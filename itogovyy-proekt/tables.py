import sqlite3

def create_tables(dbName="base.db"):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()

    # Таблица пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0,
        customer_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
    """)

    # Таблица товаров
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        company_id INTEGER NOT NULL,
        price INTEGER NOT NULL,  -- цена в копейках
        total_quantity INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id),
        FOREIGN KEY (company_id) REFERENCES companies(id)
    )
    """)

    # Таблица категорий
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # Таблица компаний
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        state TEXT NOT NULL
    )
    """)

    # Таблица чеков
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cheques (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_date TEXT NOT NULL,
        customer_id INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        pup_id INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (pup_id) REFERENCES pups(id)
    )
    """)

    # Таблица деталей продажи
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES cheques(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    # Таблица корзины покупок
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    # Таблица покупателей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        address TEXT NOT NULL
    )
    """)

    # Таблица пунктов выдачи
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Таблицы успешно созданы")