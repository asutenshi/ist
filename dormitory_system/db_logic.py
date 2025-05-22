import sqlite3

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
    
    def get_students(self):
        self.cursor.execute("""
            SELECT s.last_name, s.first_name, s.middle_name, s.academic_score,
                   r.dormitory_id, r.room_number 
            FROM students s
            JOIN student_room_assignments sra ON s.id = sra.student_id
            JOIN rooms r ON sra.room_id = r.id
        """)
            # JOIN dormitories d ON r.dormitory_id = d.id
        return self.cursor.fetchall()

    def get_students_by_dormitory(self, dormitory_name):
        self.cursor.execute(f"""
            SELECT s.last_name, s.first_name, s.middle_name, s.academic_score,
                   d.name AS dormitory_name, r.room_number 
            FROM students s
            JOIN student_room_assignments sra ON s.id = sra.student_id
            JOIN rooms r ON sra.room_id = r.id
            JOIN dormitories d ON r.dormitory_id = d.id
            WHERE dormitory_name = ?
        """, (dormitory_name,))
        return self.cursor.fetchall()