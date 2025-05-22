import db_logic

db = db_logic.DatabaseManager()
db.connect()
students = db.get_students()
print(students)
print()
print(db.get_students_by_dormitory('Общежитие №3'))