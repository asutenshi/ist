# %%
import sqlite3
import pandas as pd

# %%
products = pd.read_csv('products.csv')
products.columns = ['id', 'department', 'product_name', 'units', 'quantity', 'price']
shops = pd.read_csv('shops.csv')
shops.columns = ['id', 'district', 'address']
transfers = pd.read_csv('transfers.csv')
transfers.columns = ['id', 'date', 'shop_id', 'product_id', 'quantity', 'operation_type']
transfers.date = pd.to_datetime(transfers.date)
transfers.date = transfers.date.dt.strftime('%Y-%m-%d')

# %%
connection = sqlite3.connect('baza.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id integer primary key NOT NULL UNIQUE,
        department TEXT NOT NULL,
        product_name TEXT NOT NULL,
        units TEXT NOT NULL,
        quantity integer NOT NULL,
        price integer NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS shops (
        id TEXT primary key NOT NULL UNIQUE,
        district TEXT NOT NULL,
        address TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transfers (
        id integer primary key NOT NULL UNIQUE,
        date TEXT NOT NULL,
        shop_id TEXT NOT NULL,
        product_id integer NOT NULL,
        quantity integer NOT NULL,
        operation_type TEXT NOT NULL,
        FOREIGN KEY(shop_id) REFERENCES shops(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    );
""")

connection.commit()

# %%
products.to_sql('products', connection, if_exists='append', index=False)
shops.to_sql('shops', connection, if_exists='append', index=False)
transfers.to_sql('transfers', connection, if_exists='append', index=False)

for table in ('products', 'shops', 'transfers'):
    cursor.execute(f'SELECT * FROM {table}')
    print(cursor.fetchall())

connection.commit()

# %%
cursor.execute("""
    SELECT
    t.id, t.date,
    s.district, s.address,
    p.product_name, p.quantity AS packing_quantity,
    t.quantity, t.operation_type
    FROM transfers t
    JOIN shops s ON t.shop_id = s.id
    JOIN products p ON t.product_id = p.id
    WHERE t.date BETWEEN '2023-09-07' AND '2023-09-22'
    AND t.operation_type = 'Продажа'
    AND s.address LIKE '%Тургенев%'
    AND p.product_name LIKE '%Шампунь%'
""")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
    SELECT
        SUM(p.quantity * t.quantity) / 1000.0 AS total
    FROM transfers t
    JOIN shops s ON t.shop_id = s.id
    JOIN products p ON t.product_id = p.id
    WHERE t.date BETWEEN '2023-09-07' and '2023-09-22'
        AND s.address LIKE '%Тургенев%'
        AND t.operation_type = 'Продажа'
        AND p.product_name LIKE '%Шампунь%'
""")
total = int(cursor.fetchall()[0][0])
print(total)
# %%
