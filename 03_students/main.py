# %%
import sqlite3
import pandas as pd

# %%

connection = sqlite3.connect('baza.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_levels (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_fields (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_types (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        id_level INTEGER NOT NULL,
        id_field INTEGER NOT NULL,
        id_type INTEGER NOT NULL,
        surname TEXT NOT NULL,
        name TEXT NOT NULL,
        mid_name TEXT NOT NULL,
        avg_mark REAL NOT NULL,
    FOREIGN KEY(id_level) REFERENCES study_levels(id),
    FOREIGN KEY(id_field) REFERENCES study_fields(id),
    FOREIGN KEY(id_type) REFERENCES study_types(id)
    );
""")

connection.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
print(tables)

for t in tables:
    print(f'Таблица {t}:')
    cursor.execute(f"PRAGMA table_info({t});")
    columns = cursor.fetchall()
    for c in columns:
        print(f' - {c[1]} ({c[2]})')

# %%
csv_files = {
    'students' : 'students.csv',
    'study_fields' : 'study_fields.csv',
    'study_levels' : 'study_levels.csv',
    'study_types' : 'study_types.csv',
}

for t_name, f_name in csv_files.items():
    df = pd.read_csv(f_name)
    df.to_sql(t_name, connection, if_exists='append', index=False)

connection.commit()

# %%
for t in tables:
    cursor.execute(f"SELECT * FROM {t}")
    print(cursor.fetchall())

# %%
cursor.execute("""
    SELECT COUNT(s.id)
    FROM students s
""")
print(f'Количество студентов: {int(cursor.fetchone()[0])}')

print()

cursor.execute("""
    SELECT COUNT(s.id), f.name
    FROM students s
    JOIN study_fields f ON s.id_field = f.id
    GROUP BY f.name
    ORDER BY COUNT(s.id) DESC
""")
for count_, field in cursor.fetchall():
    print(f'На направлении {field} обучается {count_} человек')

print()

cursor.execute("""
    SELECT COUNT(s.id), l.name
    FROM students s
    JOIN study_levels l ON s.id_level = l.id
    GROUP BY l.name
    ORDER BY COUNT(s.id) DESC
""")
for count_, field in cursor.fetchall():
    print(f'На уровне {field} обучается {count_} человек')

print()

for def_ in ('MAX', 'MIN', 'AVG'):
    cursor.execute(f"""
        SELECT {def_}(s.avg_mark), f.name
        FROM students s
        JOIN study_fields f ON s.id_field = f.id
        GROUP BY f.name
    """)

    print_def = {
        'MAX' : 'Максимальный',
        'MIN' : 'Минимальный',
        'AVG' : 'Средний',
    }

    for mark, field in cursor.fetchall():
        print(f'{print_def[def_]} балл по направлению {field}: {round(mark, 2)}')
    print()

col_ids = {
    'study_levels' : 'id_level',
    'study_fields' : 'id_field',
    'study_types' : 'id_type'
}

for table in tables[:-1]:
    cursor.execute(f"""
        SELECT AVG(s.avg_mark), t.name
        FROM students s
        JOIN {table} t ON s.{col_ids[table]} = t.id
        GROUP BY t.name
    """)

    prints = {
    'study_levels' : 'уровням обучения',
    'study_fields' : 'направлениям обучения',
    'study_types' : 'типам обучения'
    }

    for mark, group in cursor.fetchall():
        print(f'Средня оценка при групперовке по {prints[table]} у группы {group}: {round(mark, 2)}')
    print()

cursor.execute("""
    SELECT s.surname, s.name, s.mid_name, s.avg_mark, f.name, t.name
    FROM students s
    JOIN study_fields f ON s.id_field = f.id
    JOIN study_types t ON s.id_type = t.id
    WHERE f.name LIKE '%Прикладная информатика%'
    AND t.name = 'Дневной'
    ORDER BY s.avg_mark DESC
    LIMIT 5
""")
for s in cursor.fetchall():
    print(f"""Студент {s[0]} {s[1]} {s[2]}, обучающийся на {s[5]} форме обучения, на направлении {s[4]}
    Выдвигается на повышенную стипендию, имея средний балл {round(s[3], 2)}""")
print()

cursor.execute("""
    SELECT COUNT(s.id), s.surname
    FROM students s
    GROUP BY s.surname
    HAVING COUNT(s.id) > 1
    ORDER BY COUNT(s.id) DESC
""")
sum_ = 0
for c, surname in cursor.fetchall():
    print(f'По фамилии {surname} имеется {c} однофамильца')
    sum_ += c
print(f'Всего однофамильцев {sum_} \n')

cursor.execute("""
    SELECT s.surname, s.name, s.mid_name, COUNT(s.id)
    FROM students s
    GROUP BY s.surname, s.name, s.mid_name
    HAVING COUNT(s.id) > 1
    ORDER BY COUNT(s.id) DESC
""")

sum_ = 0
for surname, name, midname, c in cursor.fetchall():
    print(f'Количество тёзек {surname} {name} {midname}: {c}')
    sum_ += c
print(f'Всего полных тёзек {sum_}')
# %%
connection.close()
# %%
