# %%
import sqlite3
import pandas as pd
import os

# %%
connection = sqlite3.connect("database/baza.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_levels (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculties (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_fields (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_types (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dormitory_statuses (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS genders (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS region_priorities (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        gender INTEGER NOT NULL,
        academic_score INTEGER NOT NULL,
        course_level INTEGER NOT NULL,
        study_level INTEGER NOT NULL,
        study_type INTEGER NOT NULL,
        region_priority INTEGER NOT NULL,
        faculty INTEGER NOT NULL,
        study_field INTEGER NOT NULL,
        dormitory_status INTEGER,
        behaviour_score INTEGER,
    FOREIGN KEY(gender) REFERENCES genders(id),
    FOREIGN KEY(study_level) REFERENCES study_levels(id),
    FOREIGN KEY(region_priority) REFERENCES region_priorities(id),
    FOREIGN KEY(faculty) REFERENCES faculties(id),
    FOREIGN KEY(study_field) REFERENCES study_fields(id),
    FOREIGN KEY(study_type) REFERENCES study_types(id),
    FOREIGN KEY(dormitory_status) REFERENCES dormitory_statuses(id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dormitories (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        address TEXT NOT NULL UNIQUE,
        capacity INTEGER NOT NULL,
        number_of_students INTEGER NOT NULL,
        evaluation INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS improvements (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        dormitory_id INTEGER NOT NULL,
        room_number TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        evaluation INTEGER NOT NULL,
        gender INTEGER NOT NULL,
        improvement INTEGER NOT NULL,
        floor INTEGER NOT NULL,
    FOREIGN KEY(dormitory_id) REFERENCES dormitories(id),
    FOREIGN KEY(gender) REFERENCES genders(id),
    FOREIGN KEY(improvement) REFERENCES improvements(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_room_assignments (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        student_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        assignment_date TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(room_id) REFERENCES rooms(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaint_levels (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        student_id INTEGER NOT NULL,
        complaint_level INTEGER NOT NULL,
        complaint_text TEXT NOT NULL,
        complaint_date TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(complaint_level) REFERENCES complaint_levels(id)
    )
""")

connection.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
print(tables)

# %%
for t in tables:
    print(f'Таблица {t}:')
    cursor.execute(f"PRAGMA table_info({t});")
    columns = cursor.fetchall()
    for c in columns:
        print(f' - {c[1]} ({c[2]})')

# %%

# ref_path = "./references/"
# ref_names = [f for f in os.listdir(ref_path) if os.path.isfile(os.path.join(ref_path, f))]

for t in tables:
    print(t)
    df = pd.read_csv(f"references/{t}.csv")
    df.to_sql(t, connection, if_exists='replace', index=False)
# %%

for t in tables:
    print(t)
    cursor.execute(f"SELECT * FROM {t};")
    print(cursor.fetchall())

# %%

cursor.execute("""
    SELECT s.last_name
    FROM students s
    JOIN student_room_assignments sra ON s.id = sra.student_id
""")
print(cursor.fetchall())
# %%
# Проверка наличия записей о студентах не только из первой общаги
print("Проверка распределения студентов по общежитиям на основе student_room_assignments:")
cursor.execute("""
    SELECT r.dormitory_id, COUNT(sra.student_id) as student_count
    FROM student_room_assignments sra
    JOIN rooms r ON sra.room_id = r.id
    GROUP BY r.dormitory_id
    ORDER BY r.dormitory_id;
""")
assignments_by_dormitory = cursor.fetchall()

if not assignments_by_dormitory:
    print("Нет данных о распределении студентов по комнатам в таблице student_room_assignments.")
else:
    print("Распределение студентов по ID общежитий (согласно student_room_assignments):")
    found_in_other_dorms = False
    has_assignments_in_dorm1 = False

    for dorm_id, count in assignments_by_dormitory:
        print(f"- Общежитие ID {dorm_id}: {count} студент(ов)")
        if dorm_id != 1 and count > 0:
            found_in_other_dorms = True
        if dorm_id == 1 and count > 0:
            has_assignments_in_dorm1 = True
    
    if found_in_other_dorms:
        print("\nВывод: В student_room_assignments.csv ЕСТЬ записи о студентах, размещенных в общежитиях ПОМИМО первого.")
    elif has_assignments_in_dorm1:
        print("\nВывод: Все студенты, указанные в student_room_assignments.csv, размещены ТОЛЬКО в первом общежитии.")
    else:
        # This case means assignments exist, but none are in dorm 1 and none are in other dorms,
        # which implies an issue or specific data configuration (e.g. only students in dorm 0 if such ID existed and was not 1)
        # Or, if assignments_by_dormitory was empty, the first `if` would catch it.
        # If assignments_by_dormitory has entries but neither condition above is met, it's an unusual state.
        print("\nВывод: Не удалось однозначно определить. Возможно, студенты размещены в общежитиях, но не в первом, или данные требуют дополнительного анализа.")

# %%
