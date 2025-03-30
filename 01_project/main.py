import sqlite3

connection = sqlite3.connect('01_project/baza.db')
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

job_titles_data = [
    (1, 'Менеджер'),
    (2, 'Разработчик'),
    (3, 'Аналитик'),
    (4, 'Дизайнер')
]

cursor.executemany("INSERT OR IGNORE INTO 'job_titles' ('id_job_title', 'name') VALUES (?, ?)", job_titles_data)

empoyees_data = [
    (1, 'Иванов', 'Иван', 2),
    (2, 'Александров', 'Александр', 1),
    (3, 'Петров', 'Петр', 3),
    (4, 'Сидоров', 'Глеб', 2),
    (5, 'Алексеев', 'Алексей', 4)
]

cursor.executemany("INSERT OR IGNORE INTO 'employees' ('id', 'surname', 'name', 'id_job_title') VALUES (?, ?, ?, ?)", empoyees_data)

connection.commit()

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

orders_data = [
    (1, 1, 1, 100, '12.12.2005', 'done'),
    (2, 2, 2, 300, '12.11.2005', 'issued'),
    (3, 3, 3, 400, '05.12.2005', 'done'),
    (4, 4, 4, 500, '11.12.2005', 'done'),
]

cursor.executemany("INSERT OR IGNORE INTO 'orders' ('id_order', 'id_customer', 'id_employee', 'sum', 'order_date', 'status') VALUES (?, ?, ?, ?, ?, ?)", orders_data)
cursor.execute("SELECT * FROM 'orders'")
orders = cursor.fetchall()
print(orders)

connection.close()