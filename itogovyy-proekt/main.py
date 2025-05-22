import sys
from PyQt5.QtWidgets import QApplication
from gui import LoginWindow
from dbmanager import DBManager

# Инициализация базы данных и создание необходимых таблиц
def init_db():
    db = DBManager()
    
    # Добавление тестовых данных, если база пуста
    conn = db._connect()
    cursor = conn.cursor()
    
    # Проверка наличия категорий
    cursor.execute("SELECT COUNT(*) as count FROM categories")
    if cursor.fetchone()['count'] == 0:
        print("Добавляем тестовые данные...")
        
        # Добавляем категории
        db.add_category("Электроника")
        db.add_category("Одежда")
        db.add_category("Продукты питания")
        db.add_category("Бытовая техника")
        
        # Добавляем компании
        db.add_company("Samsung", "Южная Корея")
        db.add_company("Apple", "США")
        db.add_company("Adidas", "Германия")
        db.add_company("Nike", "США")
        
        # Добавляем пункты выдачи
        db.add_pup("ул. Ленина, 10")
        db.add_pup("ул. Пушкина, 15")
        db.add_pup("ул. Гагарина, 25")
        
        # Добавляем товары (цены в копейках)
        db.add_product("Смартфон Galaxy S21", 1, 1, 8999900, 10)
        db.add_product("iPhone 13", 1, 2, 9499900, 5)
        db.add_product("Футболка спортивная", 2, 3, 299900, 50)
        db.add_product("Кроссовки беговые", 2, 4, 549900, 20)
        db.add_product("Молоко 3.2%", 3, 1, 8900, 100)
        db.add_product("Хлеб белый", 3, 2, 4500, 200)
        db.add_product("Холодильник двухкамерный", 4, 1, 4999900, 3)
        db.add_product("Микроволновая печь", 4, 2, 1499900, 15)
        
        print("Тестовые данные добавлены успешно!")
    
    conn.close()

if __name__ == "__main__":
    # Инициализация базы данных
    init_db()
    
    # Запуск приложения
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())