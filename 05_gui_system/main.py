import sys
from PyQt5.QtWidgets import QApplication
from gui_logic import ShopApp

def main():
    # Создаем экземпляр приложения Qt
    app = QApplication(sys.argv)
    
    # Создаем главное окно приложения
    window = ShopApp()
    
    # Показываем окно
    window.show()
    
    # Запускаем цикл обработки событий приложения
    # и возвращаем код выхода при завершении
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()