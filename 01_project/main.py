# %%
import sqlite3

connection = sqlite3.connect('baza.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS `job_titles` (
        `id_job_title` integer primary key NOT NULL UNIQUE,
        `name` TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS `employees` (
        `id` integer primary key NOT NULL UNIQUE,
        `surname` TEXT NOT NULL,
        `name` TEXT NOT NULL,
        `id_job_title` INTEGER NOT NULL,
    FOREIGN KEY(`id_job_title`) REFERENCES `job_titles`(`id_job_title`)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS `orders` (
        `id_order` integer primary key NOT NULL UNIQUE,
        `id_customer` INTEGER NOT NULL,
        `id_employee` INTEGER NOT NULL,
        `sum` INTEGER NOT NULL,
        `order_date` REAL NOT NULL,
        `status` TEXT NOT NULL,
    FOREIGN KEY(`id_customer`) REFERENCES `customers`(`id`),
    FOREIGN KEY(`id_employee`) REFERENCES `employees`(`id`)
    );
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS `customers` (
        `id` integer primary key NOT NULL UNIQUE,
        `company` TEXT NOT NULL,
        `phone_number` TEXT NOT NULL
    );
''')

connection.commit()

# %%
job_titles_data = [
    (1, 'Менеджер'),
    (2, 'Разработчик'),
    (3, 'Аналитик'),
    (4, 'Дизайнер'),
    (5, 'Тестировщик'),
    (6, 'DevOps-инженер'),
    (7, 'Продакт-менеджер')
]


empoyees_data = [
    (1, 'Иванов', 'Иван', 2),
    (2, 'Александров', 'Александр', 1),
    (3, 'Петров', 'Петр', 3),
    (4, 'Сидоров', 'Глеб', 2),
    (5, 'Алексеев', 'Алексей', 4),
    (6, 'Федоров', 'Федор', 5),
    (7, 'Николаев', 'Николай', 6),
    (8, 'Козлов', 'Дмитрий', 7),
    (9, 'Орлов', 'Сергей', 2),
    (10, 'Титов', 'Тимофей', 3)
]


customers_data = [
    (1, 'mlata', '888'),
    (2, 'hqd', '777'),
    (3, 'sesla', '923'),
    (4, 'ozono', '428'),
    (5, 'vilbiries', '928'),
    (6, 'yandeks', '911'),
    (7, 'kubmarket', '912'),
    (8, 'lamda', '913'),
    (9, 'sofone', '914'),
    (10, 'krutco', '915')
]


orders_data = [
    (1, 1, 1, 100, '12.12.2005', 'done'),
    (2, 2, 2, 300, '12.11.2005', 'issued'),
    (3, 3, 3, 400, '05.12.2005', 'done'),
    (4, 4, 4, 500, '11.12.2005', 'done'),
    (5, 5, 5, 150, '10.12.2005', 'canceled'),
    (6, 6, 6, 700, '13.12.2005', 'done'),
    (7, 7, 7, 320, '14.12.2005', 'issued'),
    (8, 8, 8, 280, '15.12.2005', 'done'),
    (9, 9, 9, 1000, '16.12.2005', 'issued'),
    (10, 10, 10, 750, '17.12.2005', 'done'),
    (11, 1, 2, 220, '18.12.2005', 'done'),
    (12, 2, 3, 330, '19.12.2005', 'canceled'),
    (13, 3, 4, 410, '20.12.2005', 'issued'),
    (14, 4, 5, 190, '21.12.2005', 'done'),
    (15, 5, 6, 600, '22.12.2005', 'issued')
]


cursor.executemany("""INSERT OR IGNORE INTO 'job_titles' 
    ('id_job_title', 'name') VALUES (?, ?)""",
     job_titles_data)

cursor.executemany("""INSERT OR IGNORE INTO 'employees'
    ('id', 'surname', 'name', 'id_job_title') VALUES (?, ?, ?, ?)""",
    empoyees_data)

cursor.executemany("""INSERT OR IGNORE INTO 'orders' 
    ('id_order', 'id_customer', 'id_employee', 'sum', 'order_date', 'status')
    VALUES (?, ?, ?, ?, ?, ?)""",
    orders_data)

cursor.executemany("""INSERT OR IGNORE INTO customers
    (id, company, phone_number)
    VALUES (?, ?, ?)""", customers_data)

connection.commit()

# %%
cursor.execute('''
    SELECT e.surname, e.name, j.name as job_title
    FROM employees e
    JOIN job_titles j ON e.id_job_title = j.id_job_title
''')
employees_with_job_titles = cursor.fetchall()

print(employees_with_job_titles)
print('Сотрудники и их должности: ')

for employee in employees_with_job_titles:
    print(f'{employee[0]} {employee[1]} - {employee[2]}')

cursor.execute(''' 
    SELECT e.surname, e.name
    FROM employees e
    JOIN job_titles j ON e.id_job_title = j.id_job_title
    WHERE j.name = 'Разработчик'
''')
developers = cursor.fetchall()

print("\nРазработчики: ")
for developer in developers:
    print(f'{developer[0]} {developer[1]}')

tables = ['orders', 'employees', 'job_titles', 'customers']

for table in tables:
    cursor.execute(f'SELECT * FROM {table}')
    print(cursor.fetchall())

# %%
cursor.execute("""
    SELECT COUNT(j.id_job_title)
    FROM job_titles j
""")
print(f'Количество должностей: {int(cursor.fetchone()[0])}')

cursor.execute("""
    SELECT MIN(o.order_date)
    FROM orders o
""")
print(f'Дата самого раннего заказа: {cursor.fetchone()[0]}')

cursor.execute("""
    SELECT MAX(o.order_date)
    FROM orders o
""")
print(f'Дата самого позднего заказа: {cursor.fetchone()[0]}')

cursor.execute("""
    SELECT SUM(o.sum)
    FROM orders o
""")
print(f'Сумма заказов в таблице orders: {str(cursor.fetchone()[0])}')

cursor.execute("""
    SELECT AVG(o.sum)
    FROM orders o
""")
print(f'Средняя сумма заказов в таблице orders: {int(cursor.fetchone()[0])}')

# %%
cursor.execute("""
    SELECT status, SUM(o.sum)
    FROM orders o
    GROUP BY o.status
""")
print(f'Сумма заказов по статусу: {cursor.fetchall()}')

cursor.execute("""
    SELECT j.name, COUNT(*)
    FROM employees e
    JOIN job_titles j ON e.id_job_title = j.id_job_title
    GROUP BY e.id_job_title
""")
print(f'Количество сотрудников по каждой должности: {cursor.fetchall()}')

cursor.execute("""
    SELECT o.order_date, AVG(o.sum)
    FROM orders o
    GROUP BY o.order_date
""")
print(f'Сумма заказов по статусу: {cursor.fetchall()}')

# %%
cursor.execute("""
    SELECT
    e.surname, e.name, j.name, SUM(o.sum)
    FROM orders o
    JOIN employees e ON o.id_employee = e.id
    JOIN job_titles j ON e.id_job_title = j.id_job_title
    JOIN customers s ON o.id_customer = s.id
    WHERE j.name = 'Разработчик'
    GROUP BY e.id
""")
print("Сумма заказов, оформленных разработчиками:")
for surname, name, job_title, total_sum in cursor.fetchall():
    print(f"{surname} {name} ({job_title}) — сумма заказов: {total_sum}₽")

print("\nЗаказы от клиента 'sesla':")
cursor.execute("""
    SELECT
    e.surname, e.name, j.name, c.company, o.sum
    FROM orders o
    JOIN employees e ON o.id_employee = e.id
    JOIN job_titles j ON e.id_job_title = j.id_job_title
    JOIN customers c ON o.id_customer = c.id
    WHERE c.company = 'sesla'
""")
for surname, name, job_title, company, order_sum in cursor.fetchall():
    print(f"Клиент: {company} — заказ на {order_sum}₽, оформил: {surname} {name} ({job_title})")

print("\nВсе выполненные заказы (статус 'done'):")
cursor.execute("""
    SELECT
    c.company, o.sum, o.order_date, o.status
    FROM orders o
    JOIN employees e ON o.id_employee = e.id
    JOIN job_titles j ON e.id_job_title = j.id_job_title
    JOIN customers c ON o.id_customer = c.id
    WHERE o.status = 'done'
""")
for company, order_sum, order_date, status in cursor.fetchall():
    print(f"{order_date}: {company} — заказ на {order_sum}₽ [{status}]")


# %%
connection.close()
# %%
