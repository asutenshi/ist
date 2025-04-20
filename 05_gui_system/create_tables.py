# %%
import sqlite3
import pandas as pd

# %%
connection = sqlite3.connect('database/baza.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        category TEXT NOT NULL UNIQUE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        id_category INTEGER NOT NULL,
        name TEXT NOT NULL UNIQUE,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
    FOREIGN KEY(id_category) REFERENCES categories(id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        date TEXT NOT NULL,
        total_price INTEGER NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        id_receipt INTEGER NOT NULL,
        id_product INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL,
    FOREIGN KEY(id_receipt) REFERENCES receipts(id),
    FOREIGN KEY(id_product) REFERENCES products(id)
    );
""")

connection.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]

# %%
categories = pd.read_csv('references/categories.csv')
products = pd.read_csv('references/products.csv')
receipts = pd.read_csv('references/receipts.csv')
receipts.date = pd.to_datetime(receipts.date)
history = pd.read_csv('references/history.csv')

for table, name in zip((categories, products, receipts, history),
                       tables):
    table.to_sql(name, connection, if_exists='append', index=False)

connection.commit()

# %%
for t in tables:
    print(f'Таблица {t}:')
    cursor.execute(f"PRAGMA table_info({t});")
    columns = cursor.fetchall()
    for c in columns:
        print(f' - {c[1]} ({c[2]})')

# %%
for t in tables:
    cursor.execute(f"SELECT * FROM {t}")
    print(cursor.fetchall())
# %%
connection.close()