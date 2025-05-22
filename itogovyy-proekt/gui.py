import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                            QComboBox, QMessageBox, QTabWidget, QSpinBox, QDialog, QFormLayout, 
                            QStackedWidget, QGroupBox, QRadioButton, QButtonGroup, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon
from dbmanager import DBManager


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Система учета и продажи товаров")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Форма входа
        form_layout = QFormLayout()
        
        self.login_field = QLineEdit()
        form_layout.addRow("Логин:", self.login_field)
        
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Пароль:", self.password_field)
        
        login_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        
        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.show_register)
        
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.register_button)
        
        layout.addLayout(form_layout)
        layout.addLayout(login_layout)
        
        # Создание admin пользователя при первом запуске
        self.create_admin()
        
        self.setLayout(layout)
        
    def create_admin(self):
        """Создает администратора при первом запуске"""
        # Проверяем, существует ли пользователь admin
        if not self.db.login_user("admin", "admin"):
            self.db.register_user("admin", "admin", "Администратор", "Системы", "Администраторская 228")
            # Устанавливаем права администратора
            conn = self.db._connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_admin = 1 WHERE login = 'admin'")
            conn.commit()
            conn.close()
        
    def login(self):
        login = self.login_field.text()
        password = self.password_field.text()
        
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
            
        user = self.db.login_user(login, password)
        
        if user:
            self.main_window = MainWindow(user)
            self.main_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
            
    def show_register(self):
        self.register_window = RegisterWindow()
        self.register_window.registerSuccess.connect(self.on_register_success)
        self.register_window.show()
        self.hide()
        
    def on_register_success(self, login, password):
        """Обрабатывает успешную регистрацию"""
        self.login_field.setText(login)
        self.password_field.setText(password)
        self.show()


class RegisterWindow(QWidget):
    from PyQt5.QtCore import pyqtSignal
    
    registerSuccess = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Регистрация нового пользователя")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Форма регистрации
        form_layout = QFormLayout()
        
        self.login_field = QLineEdit()
        form_layout.addRow("Логин:", self.login_field)
        
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Пароль:", self.password_field)
        
        self.name_field = QLineEdit()
        form_layout.addRow("Имя:", self.name_field)
        
        self.surname_field = QLineEdit()
        form_layout.addRow("Фамилия:", self.surname_field)
        
        self.address_field = QLineEdit()
        form_layout.addRow("Адрес:", self.address_field)
        
        button_layout = QHBoxLayout()
        
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)
        
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.back_to_login)
        
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.back_button)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def register(self):
        login = self.login_field.text()
        password = self.password_field.text()
        name = self.name_field.text()
        surname = self.surname_field.text()
        address = self.address_field.text()
        
        if not all([login, password, name, surname, address]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
            
        success = self.db.register_user(login, password, name, surname, address)
        
        if success:
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно")
            self.registerSuccess.emit(login, password)
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")
            
    def back_to_login(self):
        from main import app
        login_window = LoginWindow()
        login_window.show()
        self.hide()


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = DBManager()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Система учета и продажи товаров")
        self.setGeometry(100, 100, 1200, 800)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout()
        
        # Информация о пользователе
        user_info = QLabel(f"Пользователь: {self.user['login']}")
        main_layout.addWidget(user_info)
        
        # Кнопка выхода
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.logout)
        main_layout.addWidget(self.logout_button, alignment=Qt.AlignRight)
        
        # Виджет с вкладками
        self.tab_widget = QTabWidget()
        
        # Добавляем основные вкладки
        self.setup_catalog_tab()
        self.setup_cart_tab()
        self.setup_orders_tab()
        
        # Если пользователь - администратор, добавляем панель администратора
        if self.user['is_admin']:
            self.setup_admin_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        central_widget.setLayout(main_layout)
        
    def setup_catalog_tab(self):
        """Настройка вкладки с каталогом товаров"""
        catalog_widget = QWidget()
        layout = QVBoxLayout()
        
        # Верхняя часть - выбор категории
        top_layout = QHBoxLayout()
        
        category_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.update_categories_combo()
        
        self.category_combo.currentIndexChanged.connect(self.load_products)
        
        top_layout.addWidget(category_label)
        top_layout.addWidget(self.category_combo)
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # Таблица с товарами
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels(["ID", "Название", "Категория", "Производитель", "Цена (руб.)", "В наличии"])
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.products_table)
        
        # Нижняя часть - добавление в корзину
        bottom_layout = QHBoxLayout()
        
        add_label = QLabel("Количество:")
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(100)
        
        self.add_to_cart_button = QPushButton("Добавить в корзину")
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        
        bottom_layout.addWidget(add_label)
        bottom_layout.addWidget(self.quantity_spin)
        bottom_layout.addWidget(self.add_to_cart_button)
        bottom_layout.addStretch()
        
        layout.addLayout(bottom_layout)
        
        catalog_widget.setLayout(layout)
        self.tab_widget.addTab(catalog_widget, "Каталог")
        
        # Загружаем товары первой категории если есть
        if self.category_combo.count() > 0:
            self.load_products()
        
    def setup_cart_tab(self):
        """Настройка вкладки с корзиной"""
        cart_widget = QWidget()
        layout = QVBoxLayout()
        
        # Таблица с товарами в корзине
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["ID", "Название", "Цена (руб.)", "Количество", "Сумма (руб.)"])
        self.cart_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.cart_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.cart_table)
        
        # Нижняя часть - итого и кнопки
        bottom_layout = QHBoxLayout()
        
        self.total_label = QLabel("Итого: 0 руб.")
        font = QFont()
        font.setBold(True)
        self.total_label.setFont(font)
        
        self.remove_button = QPushButton("Удалить из корзины")
        self.remove_button.clicked.connect(self.remove_from_cart)
        
        self.checkout_button = QPushButton("Оформить заказ")
        self.checkout_button.clicked.connect(self.show_checkout_dialog)
        
        bottom_layout.addWidget(self.total_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.remove_button)
        bottom_layout.addWidget(self.checkout_button)
        
        layout.addLayout(bottom_layout)
        
        cart_widget.setLayout(layout)
        self.tab_widget.addTab(cart_widget, "Корзина")
        
        # Загружаем содержимое корзины
        self.load_cart()
        
    def setup_orders_tab(self):
        """Настройка вкладки с заказами пользователя"""
        orders_widget = QWidget()
        layout = QVBoxLayout()
        
        # Таблица с заказами
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Дата", "Сумма (руб.)", "Пункт выдачи"])
        self.orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.orders_table)
        
        # Кнопка просмотра деталей заказа
        self.view_order_button = QPushButton("Просмотреть детали заказа")
        self.view_order_button.clicked.connect(self.view_order_details)
        
        layout.addWidget(self.view_order_button, alignment=Qt.AlignRight)
        
        orders_widget.setLayout(layout)
        self.tab_widget.addTab(orders_widget, "Мои заказы")
        
        # Загружаем заказы пользователя
        self.load_orders()
        
    def setup_admin_tab(self):
        """Настройка вкладки для администратора"""
        self.admin_tab = QTabWidget()
        
        # Настраиваем вкладки администратора
        self.setup_admin_products()
        self.setup_admin_categories()
        self.setup_admin_companies()
        self.setup_admin_users()
        self.setup_admin_pups()
        
        self.tab_widget.addTab(self.admin_tab, "Администрирование")
        
    def setup_admin_products(self):
        """Настройка вкладки управления товарами"""
        products_widget = QWidget()
        layout = QVBoxLayout()
        
        # Таблица с товарами
        self.admin_products_table = QTableWidget()
        self.admin_products_table.setColumnCount(6)
        self.admin_products_table.setHorizontalHeaderLabels(["ID", "Название", "Категория", "Производитель", "Цена (руб.)", "В наличии"])
        self.admin_products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.admin_products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.admin_products_table)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.add_product_button = QPushButton("Добавить")
        self.add_product_button.clicked.connect(self.add_product_dialog)
        
        self.edit_product_button = QPushButton("Редактировать")
        self.edit_product_button.clicked.connect(self.edit_product_dialog)
        
        self.delete_product_button = QPushButton("Удалить")
        self.delete_product_button.clicked.connect(self.delete_product)
        
        buttons_layout.addWidget(self.add_product_button)
        buttons_layout.addWidget(self.edit_product_button)
        buttons_layout.addWidget(self.delete_product_button)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        products_widget.setLayout(layout)
        self.admin_tab.addTab(products_widget, "Товары")
        
        # Загружаем список товаров
        self.load_admin_products()
        
    def setup_admin_categories(self):
        """Настройка вкладки управления категориями"""
        categories_widget = QWidget()
        layout = QVBoxLayout()
        
        # Таблица с категориями
        self.admin_categories_table = QTableWidget()
        self.admin_categories_table.setColumnCount(2)
        self.admin_categories_table.setHorizontalHeaderLabels(["ID", "Название"])
        self.admin_categories_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.admin_categories_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.admin_categories_table)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.add_category_button = QPushButton("Добавить")
        self.add_category_button.clicked.connect(self.add_category_dialog)
        
        self.edit_category_button = QPushButton("Редактировать")
        self.edit_category_button.clicked.connect(self.edit_category_dialog)
        
        self.delete_category_button = QPushButton("Удалить")
        self.delete_category_button.clicked.connect(self.delete_category)
        
        buttons_layout.addWidget(self.add_category_button)
        buttons_layout.addWidget(self.edit_category_button)
        buttons_layout.addWidget(self.delete_category_button)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        categories_widget.setLayout(layout)
        self.admin_tab.addTab(categories_widget, "Категории")
        
        # Загружаем список категорий
        self.load_admin_categories()
        
    def setup_admin_companies(self):
        """Настройка вкладки управления компаниями"""
        companies_widget = QWidget()
        layout = QVBoxLayout()
        
        # Таблица с компаниями
        self.admin_companies_table = QTableWidget()
        self.admin_companies_table.setColumnCount(3)
        self.admin_companies_table.setHorizontalHeaderLabels(["ID", "Название", "Страна"])
        self.admin_companies_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.admin_companies_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.admin_companies_table)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.add_company_button = QPushButton("Добавить")
        self.add_company_button.clicked.connect(self.add_company_dialog)
        
        self.edit_company_button = QPushButton("Редактировать")
        self.edit_company_button.clicked.connect(self.edit_company_dialog)
        
        self.delete_company_button = QPushButton("Удалить")
        self.delete_company_button.clicked.connect(self.delete_company)
        
        buttons_layout.addWidget(self.add_company_button)
        buttons_layout.addWidget(self.edit_company_button)
        buttons_layout.addWidget(self.delete_company_button)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        companies_widget.setLayout(layout)
        self.admin_tab.addTab(companies_widget, "Компании")
        
        # Загружаем список компаний
        self.load_admin_companies()
        
    def setup_admin_users(self):
        """Настройка вкладки управления пользователями"""
        users_widget = QWidget()
        layout = QVBoxLayout()
        
        # Таблица с пользователями
        self.admin_users_table = QTableWidget()
        self.admin_users_table.setColumnCount(5)
        self.admin_users_table.setHorizontalHeaderLabels(["ID", "Логин", "Имя", "Фамилия", "Адрес"])
        self.admin_users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.admin_users_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.admin_users_table)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.view_user_button = QPushButton("Просмотреть")
        self.view_user_button.clicked.connect(self.view_user_details)
        
        buttons_layout.addWidget(self.view_user_button)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        users_widget.setLayout(layout)
        self.admin_tab.addTab(users_widget, "Пользователи")
        
        # Загружаем список пользователей
        self.load_admin_users()
        
    def setup_admin_pups(self):
        """Настройка вкладки управления пунктами выдачи"""
        pups_widget = QWidget()
        layout = QVBoxLayout()
        
        # Таблица с пунктами выдачи
        self.admin_pups_table = QTableWidget()
        self.admin_pups_table.setColumnCount(2)
        self.admin_pups_table.setHorizontalHeaderLabels(["ID", "Адрес"])
        self.admin_pups_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.admin_pups_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.admin_pups_table)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.add_pup_button = QPushButton("Добавить")
        self.add_pup_button.clicked.connect(self.add_pup_dialog)
        
        self.edit_pup_button = QPushButton("Редактировать")
        self.edit_pup_button.clicked.connect(self.edit_pup_dialog)
        
        self.delete_pup_button = QPushButton("Удалить")
        self.delete_pup_button.clicked.connect(self.delete_pup)
        
        buttons_layout.addWidget(self.add_pup_button)
        buttons_layout.addWidget(self.edit_pup_button)
        buttons_layout.addWidget(self.delete_pup_button)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        pups_widget.setLayout(layout)
        self.admin_tab.addTab(pups_widget, "Пункты выдачи")
        
        # Загружаем список пунктов выдачи
        self.load_admin_pups()
        
    def update_categories_combo(self):
        """Обновление списка категорий в комбобоксе"""
        self.category_combo.clear()
        categories = self.db.get_all_categories()
        
        if categories:
            for category in categories:
                self.category_combo.addItem(category['name'], category['id'])
    
    def load_products(self):
        """Загрузка товаров по выбранной категории"""
        if self.category_combo.currentIndex() < 0:
            return
            
        category_id = self.category_combo.currentData()
        products = self.db.get_products_by_category(category_id)
        
        self.products_table.setRowCount(0)
        
        for row, product in enumerate(products):
            self.products_table.insertRow(row)
            self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.products_table.setItem(row, 1, QTableWidgetItem(product['name']))
            self.products_table.setItem(row, 2, QTableWidgetItem(product['category_name']))
            self.products_table.setItem(row, 3, QTableWidgetItem(product['company_name']))
            
            # Преобразуем цену из копеек в рубли для отображения
            price_rub = product['price'] / 100
            self.products_table.setItem(row, 4, QTableWidgetItem(f"{price_rub:.2f}"))
            
            self.products_table.setItem(row, 5, QTableWidgetItem(str(product['total_quantity'])))
        
        self.products_table.resizeColumnsToContents()
        
    def add_to_cart(self):
        """Добавление товара в корзину"""
        selected_rows = self.products_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для добавления в корзину")
            return
            
        row = selected_rows[0].row()
        product_id = int(self.products_table.item(row, 0).text())
        quantity = self.quantity_spin.value()
        
        # Проверяем доступное количество
        available = int(self.products_table.item(row, 5).text())
        
        if quantity > available:
            QMessageBox.warning(self, "Ошибка", "Недостаточно товара на складе")
            return
            
        success = self.db.add_to_cart(self.user['id'], product_id, quantity)
        
        if success:
            QMessageBox.information(self, "Успех", "Товар добавлен в корзину")
            # Обновляем вкладку с корзиной
            self.load_cart()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить товар в корзину")
            
    def load_cart(self):
        """Загрузка содержимого корзины"""
        cart_items = self.db.get_cart(self.user['id'])
        
        self.cart_table.setRowCount(0)
        
        for row, item in enumerate(cart_items):
            self.cart_table.insertRow(row)
            self.cart_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.cart_table.setItem(row, 1, QTableWidgetItem(item['name']))
            
            # Преобразуем цену из копеек в рубли для отображения
            price_rub = item['price'] / 100
            self.cart_table.setItem(row, 2, QTableWidgetItem(f"{price_rub:.2f}"))
            
            self.cart_table.setItem(row, 3, QTableWidgetItem(str(item['quantity'])))
            
            # Преобразуем общую цену из копеек в рубли для отображения
            total_price_rub = item['total_price'] / 100
            self.cart_table.setItem(row, 4, QTableWidgetItem(f"{total_price_rub:.2f}"))
        
        self.cart_table.resizeColumnsToContents()
        
        # Обновляем общую сумму
        total = self.db.get_cart_total(self.user['id'])
        total_rub = total / 100
        self.total_label.setText(f"Итого: {total_rub:.2f} руб.")
        
    def remove_from_cart(self):
        """Удаление товара из корзины"""
        selected_rows = self.cart_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления из корзины")
            return
            
        row = selected_rows[0].row()
        cart_id = int(self.cart_table.item(row, 0).text())
        
        self.db.remove_from_cart(cart_id)
        
        # Обновляем корзину
        self.load_cart()
        
    def show_checkout_dialog(self):
        """Показывает диалог оформления заказа"""
        cart_items = self.db.get_cart(self.user['id'])
        
        if not cart_items:
            QMessageBox.warning(self, "Ошибка", "Корзина пуста")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Оформление заказа")
        
        layout = QVBoxLayout()
        
        # Общая информация о заказе
        total = self.db.get_cart_total(self.user['id'])
        total_rub = total / 100
        
        info_label = QLabel(f"Общая сумма заказа: {total_rub:.2f} руб.")
        layout.addWidget(info_label)
        
        # Выбор пункта выдачи
        pup_layout = QFormLayout()
        self.pup_combo = QComboBox()
        
        pups = self.db.get_all_pups()
        for pup in pups:
            self.pup_combo.addItem(pup['address'], pup['id'])
            
        pup_layout.addRow("Пункт выдачи:", self.pup_combo)
        layout.addLayout(pup_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        confirm_button = QPushButton("Подтвердить заказ")
        confirm_button.clicked.connect(lambda: self.confirm_order(dialog))
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(dialog.reject)
        
        buttons_layout.addWidget(confirm_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
        
    def confirm_order(self, dialog):
        """Подтверждает оформление заказа"""
        pup_id = self.pup_combo.currentData()
        
        if not pup_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пункт выдачи")
            return
            
        sale_id = self.db.checkout(self.user['id'], pup_id)
        
        if sale_id:
            QMessageBox.information(self, "Успех", f"Заказ №{sale_id} успешно оформлен")
            dialog.accept()
            
            # Обновляем корзину и заказы
            self.load_cart()
            self.load_orders()
            self.load_products()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось оформить заказ")
            
    def load_orders(self):
        """Загрузка заказов пользователя"""
        orders = self.db.get_user_cheques(self.user['id'])
        
        self.orders_table.setRowCount(0)
        
        for row, order in enumerate(orders):
            self.orders_table.insertRow(row)
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            self.orders_table.setItem(row, 1, QTableWidgetItem(order['sale_date']))
            
            # Преобразуем сумму из копеек в рубли для отображения
            total_price_rub = order['total_price'] / 100
            self.orders_table.setItem(row, 2, QTableWidgetItem(f"{total_price_rub:.2f}"))
            
            self.orders_table.setItem(row, 3, QTableWidgetItem(order['pickup_address']))
        
        self.orders_table.resizeColumnsToContents()
        
    def view_order_details(self):
        """Просмотр деталей заказа"""
        selected_rows = self.orders_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для просмотра деталей")
            return
            
        row = selected_rows[0].row()
        order_id = int(self.orders_table.item(row, 0).text())
        
        order = self.db.get_cheque_details(order_id)
        
        if not order:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить информацию о заказе")
            return
            
        # Создаем диалог с деталями заказа
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Детали заказа №{order_id}")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        
        # Информация о заказе
        order_date = QLabel(f"Дата: {order['sale_date']}")
        customer = QLabel(f"Заказчик: {order['name']} {order['surname']}")
        address = QLabel(f"Адрес заказчика: {order['address']}")
        pickup = QLabel(f"Пункт выдачи: {order['pickup_address']}")
        
        # Преобразуем сумму из копеек в рубли для отображения
        total_price_rub = order['total_price'] / 100
        total = QLabel(f"Общая сумма: {total_price_rub:.2f} руб.")
        
        layout.addWidget(order_date)
        layout.addWidget(customer)
        layout.addWidget(address)
        layout.addWidget(pickup)
        layout.addWidget(total)
        
        # Таблица с товарами
        items_table = QTableWidget()
        items_table.setColumnCount(3)
        items_table.setHorizontalHeaderLabels(["Название", "Количество", "Цена (руб.)"])
        
        for row, item in enumerate(order['items']):
            items_table.insertRow(row)
            items_table.setItem(row, 0, QTableWidgetItem(item['name']))
            items_table.setItem(row, 1, QTableWidgetItem(str(item['quantity'])))
            
            # Преобразуем цену из копеек в рубли для отображения
            price_rub = item['price'] / 100
            items_table.setItem(row, 2, QTableWidgetItem(f"{price_rub:.2f}"))
            
        items_table.resizeColumnsToContents()
        layout.addWidget(items_table)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button, alignment=Qt.AlignRight)
        
        dialog.setLayout(layout)
        dialog.exec_()
        
    def logout(self):
        """Выход из системы"""
        login_window = LoginWindow()
        login_window.show()
        self.close()
    
    def add_product_dialog(self):
        """Открывает диалог для добавления нового товара"""
        dialog = ProductDialog(self, self.db)
        if dialog.exec_():
            QMessageBox.information(self, "Успех", "Товар успешно добавлен")
            self.load_admin_products()  # Обновляем список товаров в админ-панели

    def edit_product_dialog(self):
        """Открывает диалог для редактирования товара"""
        selected_rows = self.admin_products_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для редактирования")
            return
            
        row = selected_rows[0].row()
        product_id = int(self.admin_products_table.item(row, 0).text())
        product = self.db.get_product(product_id)
        
        if not product:
            QMessageBox.warning(self, "Ошибка", "Товар не найден")
            return
            
        dialog = ProductDialog(self, self.db, product)
        if dialog.exec_():
            QMessageBox.information(self, "Успех", "Товар успешно обновлен")
            self.load_admin_products()  # Обновляем список товаров
            
    def delete_product(self):
        """Удаляет выбранный товар"""
        selected_rows = self.admin_products_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления")
            return
            
        row = selected_rows[0].row()
        product_id = int(self.admin_products_table.item(row, 0).text())
        product_name = self.admin_products_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить товар '{product_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.db.delete_product(product_id)
            if success:
                QMessageBox.information(self, "Успех", "Товар успешно удален")
                self.load_admin_products()  # Обновляем список товаров
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить товар")
                
    def load_admin_products(self):
        """Загрузка списка товаров в админ-панель"""
        products = self.db.get_all_products()
        
        self.admin_products_table.setRowCount(0)
        
        for row, product in enumerate(products):
            self.admin_products_table.insertRow(row)
            self.admin_products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.admin_products_table.setItem(row, 1, QTableWidgetItem(product['name']))
            self.admin_products_table.setItem(row, 2, QTableWidgetItem(product['category_name']))
            self.admin_products_table.setItem(row, 3, QTableWidgetItem(product['company_name']))
            
            # Преобразуем цену из копеек в рубли для отображения
            price_rub = product['price'] / 100
            self.admin_products_table.setItem(row, 4, QTableWidgetItem(f"{price_rub:.2f}"))
            
            self.admin_products_table.setItem(row, 5, QTableWidgetItem(str(product['total_quantity'])))
        
        self.admin_products_table.resizeColumnsToContents()
        
    def add_category_dialog(self):
        """Открывает диалог для добавления новой категории"""
        dialog = CategoryDialog(self, self.db)
        if dialog.exec_():
            QMessageBox.information(self, "Успех", "Категория успешно добавлена")
            self.load_admin_categories()
            self.update_categories_combo()  # Обновляем комбобокс в каталоге
            
    def edit_category_dialog(self):
        """Открывает диалог для редактирования категории"""
        selected_rows = self.admin_categories_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для редактирования")
            return
            
        row = selected_rows[0].row()
        category_id = int(self.admin_categories_table.item(row, 0).text())
        category_name = self.admin_categories_table.item(row, 1).text()
        
        # Создаем объект категории для передачи в диалог
        category = {'id': category_id, 'name': category_name}
        
        dialog = CategoryDialog(self, self.db, category)
        if dialog.exec_():
            QMessageBox.information(self, "Успех", "Категория успешно обновлена")
            self.load_admin_categories()
            self.update_categories_combo()  # Обновляем комбобокс в каталоге
            
    def delete_category(self):
        """Удаляет выбранную категорию"""
        selected_rows = self.admin_categories_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления")
            return
            
        row = selected_rows[0].row()
        category_id = int(self.admin_categories_table.item(row, 0).text())
        category_name = self.admin_categories_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить категорию '{category_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.db.delete_category(category_id)
            if success:
                QMessageBox.information(self, "Успех", "Категория успешно удалена")
                self.load_admin_categories()
                self.update_categories_combo()  # Обновляем комбобокс в каталоге
            else:
                QMessageBox.warning(self, "Ошибка", "Невозможно удалить категорию, на которую ссылаются товары")
                
    def load_admin_categories(self):
        """Загрузка списка категорий в админ-панель"""
        categories = self.db.get_all_categories()
        
        self.admin_categories_table.setRowCount(0)
        
        for row, category in enumerate(categories):
            self.admin_categories_table.insertRow(row)
            self.admin_categories_table.setItem(row, 0, QTableWidgetItem(str(category['id'])))
            self.admin_categories_table.setItem(row, 1, QTableWidgetItem(category['name']))
        
        self.admin_categories_table.resizeColumnsToContents()
        
    def add_company_dialog(self):
        """Открывает диалог для добавления новой компании"""
        dialog = CompanyDialog(self, self.db)
        if dialog.exec_():
            QMessageBox.information(self, "Успех", "Компания успешно добавлена")
            self.load_admin_companies()
            
    def edit_company_dialog(self):
        """Открывает диалог для редактирования компании"""
        selected_rows = self.admin_companies_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите компанию для редактирования")
            return
            
        row = selected_rows[0].row()
        company_id = int(self.admin_companies_table.item(row, 0).text())
        company_name = self.admin_companies_table.item(row, 1).text()
        company_state = self.admin_companies_table.item(row, 2).text()
        
        # Создаем объект компании для передачи в диалог
        company = {'id': company_id, 'name': company_name, 'state': company_state}
        
        dialog = CompanyDialog(self, self.db, company)
        if dialog.exec_():
            QMessageBox.information(self, "Успех", "Компания успешно обновлена")
            self.load_admin_companies()
            
    def delete_company(self):
        """Удаляет выбранную компанию"""
        selected_rows = self.admin_companies_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите компанию для удаления")
            return
            
        row = selected_rows[0].row()
        company_id = int(self.admin_companies_table.item(row, 0).text())
        company_name = self.admin_companies_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить компанию '{company_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.db.delete_company(company_id)
            if success:
                QMessageBox.information(self, "Успех", "Компания успешно удалена")
                self.load_admin_companies()
            else:
                QMessageBox.warning(self, "Ошибка", "Невозможно удалить компанию, на которую ссылаются товары")
                
    def load_admin_companies(self):
        """Загрузка списка компаний в админ-панель"""
        companies = self.db.get_all_companies()
        
        self.admin_companies_table.setRowCount(0)
        
        for row, company in enumerate(companies):
            self.admin_companies_table.insertRow(row)
            self.admin_companies_table.setItem(row, 0, QTableWidgetItem(str(company['id'])))
            self.admin_companies_table.setItem(row, 1, QTableWidgetItem(company['name']))
            self.admin_companies_table.setItem(row, 2, QTableWidgetItem(company['state']))
        
        self.admin_companies_table.resizeColumnsToContents()
        
    def view_user_details(self):
        """Просмотр деталей пользователя"""
        selected_rows = self.admin_users_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для просмотра")
            return
            
        row = selected_rows[0].row()
        user_id = int(self.admin_users_table.item(row, 0).text())
        
        user = self.db.get_user_details(user_id)
        
        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return
            
        # Отображаем информацию о пользователе
        info = f"ID: {user['id']}\n"
        info += f"Логин: {user['login']}\n"
        info += f"Администратор: {'Да' if user['is_admin'] else 'Нет'}\n"
        info += f"Имя: {user['name']}\n"
        info += f"Фамилия: {user['surname']}\n"
        info += f"Адрес: {user['address']}"
        
        QMessageBox.information(self, "Информация о пользователе", info)
        
    def load_admin_users(self):
        """Загрузка списка пользователей в админ-панель"""
        conn = self.db._connect()
        cursor = conn.cursor()
        
        # Получаем информацию о всех пользователях с их данными
        cursor.execute(
            """
            SELECT u.id, u.login, c.name, c.surname, c.address
            FROM users u
            JOIN customers c ON u.customer_id = c.id
            """
        )
        
        users = cursor.fetchall()
        conn.close()
        
        self.admin_users_table.setRowCount(0)
        
        for row, user in enumerate(users):
            self.admin_users_table.insertRow(row)
            self.admin_users_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.admin_users_table.setItem(row, 1, QTableWidgetItem(user['login']))
            self.admin_users_table.setItem(row, 2, QTableWidgetItem(user['name']))
            self.admin_users_table.setItem(row, 3, QTableWidgetItem(user['surname']))
            self.admin_users_table.setItem(row, 4, QTableWidgetItem(user['address']))
            
        self.admin_users_table.resizeColumnsToContents()
        
    def add_pup_dialog(self):
        """Открывает диалог для добавления нового пункта выдачи"""
        dialog = PupDialog(self, self.db)
        if dialog.exec_():
            QMessageBox.information(self, "Успех", "Пункт выдачи успешно добавлен")
            self.load_admin_pups()
            
    def edit_pup_dialog(self):
        """Открывает диалог для редактирования пункта выдачи"""
        selected_rows = self.admin_pups_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите пункт выдачи для редактирования")
            return
            
        row = selected_rows[0].row()
        pup_id = int(self.admin_pups_table.item(row, 0).text())
        pup_address = self.admin_pups_table.item(row, 1).text()
        
        # Создаем объект пункта выдачи для передачи в диалог
        pup = {'id': pup_id, 'address': pup_address}
        
        dialog = PupDialog(self, self.db, pup)
        if dialog.exec_():
            QMessageBox.information(self, "Успех", "Пункт выдачи успешно обновлен")
            self.load_admin_pups()
            
    def delete_pup(self):
        """Удаляет выбранный пункт выдачи"""
        selected_rows = self.admin_pups_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите пункт выдачи для удаления")
            return
            
        row = selected_rows[0].row()
        pup_id = int(self.admin_pups_table.item(row, 0).text())
        pup_address = self.admin_pups_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить пункт выдачи '{pup_address}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.db.delete_pup(pup_id)
            if success:
                QMessageBox.information(self, "Успех", "Пункт выдачи успешно удален")
                self.load_admin_pups()
            else:
                QMessageBox.warning(self, "Ошибка", "Невозможно удалить пункт выдачи, который используется в заказах")
                
    def load_admin_pups(self):
        """Загрузка списка пунктов выдачи в админ-панель"""
        pups = self.db.get_all_pups()
        
        self.admin_pups_table.setRowCount(0)
        
        for row, pup in enumerate(pups):
            self.admin_pups_table.insertRow(row)
            self.admin_pups_table.setItem(row, 0, QTableWidgetItem(str(pup['id'])))
            self.admin_pups_table.setItem(row, 1, QTableWidgetItem(pup['address']))
            
        self.admin_pups_table.resizeColumnsToContents()

# Диалоги администратора
class ProductDialog(QDialog):
    def __init__(self, parent, db, product=None):
        super().__init__(parent)
        self.db = db
        self.product = product
        self.init_ui()
        
    def init_ui(self):
        if self.product:
            self.setWindowTitle("Редактирование товара")
        else:
            self.setWindowTitle("Добавление товара")
            
        layout = QFormLayout()
        
        self.name_field = QLineEdit()
        layout.addRow("Название:", self.name_field)
        
        self.category_combo = QComboBox()
        categories = self.db.get_all_categories()
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])
        layout.addRow("Категория:", self.category_combo)
        
        self.company_combo = QComboBox()
        companies = self.db.get_all_companies()
        for company in companies:
            self.company_combo.addItem(company['name'], company['id'])
        layout.addRow("Производитель:", self.company_combo)
        
        self.price_field = QLineEdit()
        layout.addRow("Цена (руб.):", self.price_field)
        
        self.quantity_field = QSpinBox()
        self.quantity_field.setMinimum(0)
        self.quantity_field.setMaximum(10000)
        layout.addRow("Количество:", self.quantity_field)
        
        buttons = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow("", buttons)
        
        self.setLayout(layout)
        
        # Если редактируем существующий товар, заполняем поля
        if self.product:
            self.name_field.setText(self.product['name'])
            
            # Находим индекс категории
            index = self.category_combo.findData(self.product['category_id'])
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
                
            # Находим индекс компании
            index = self.company_combo.findData(self.product['company_id'])
            if index >= 0:
                self.company_combo.setCurrentIndex(index)
                
            # Преобразуем цену из копеек в рубли для отображения
            price_rub = self.product['price'] / 100
            self.price_field.setText(f"{price_rub:.2f}")
            
            self.quantity_field.setValue(self.product['total_quantity'])
            
    def save(self):
        name = self.name_field.text()
        category_id = self.category_combo.currentData()
        company_id = self.company_combo.currentData()
        
        try:
            # Преобразуем цену из рублей в копейки для хранения
            price_rub = float(self.price_field.text().replace(",", "."))
            price_kop = int(price_rub * 100)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную цену")
            return
            
        quantity = self.quantity_field.value()
        
        if not all([name, category_id, company_id]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
            
        if self.product:
            # Обновляем существующий товар
            self.db.update_product(
                self.product['id'], name, category_id, company_id, price_kop, quantity
            )
        else:
            # Добавляем новый товар
            self.db.add_product(name, category_id, company_id, price_kop, quantity)
            
        self.accept()


class CategoryDialog(QDialog):
    def __init__(self, parent, db, category=None):
        super().__init__(parent)
        self.db = db
        self.category = category
        self.init_ui()
        
    def init_ui(self):
        if self.category:
            self.setWindowTitle("Редактирование категории")
        else:
            self.setWindowTitle("Добавление категории")
            
        layout = QFormLayout()
        
        self.name_field = QLineEdit()
        layout.addRow("Название:", self.name_field)
        
        buttons = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow("", buttons)
        
        self.setLayout(layout)
        
        # Если редактируем существующую категорию, заполняем поля
        if self.category:
            self.name_field.setText(self.category['name'])
            
    def save(self):
        name = self.name_field.text()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название категории")
            return
            
        if self.category:
            # Обновляем существующую категорию
            self.db.update_category(self.category['id'], name)
        else:
            # Добавляем новую категорию
            self.db.add_category(name)
            
        self.accept()


class CompanyDialog(QDialog):
    def __init__(self, parent, db, company=None):
        super().__init__(parent)
        self.db = db
        self.company = company
        self.init_ui()
        
    def init_ui(self):
        if self.company:
            self.setWindowTitle("Редактирование компании")
        else:
            self.setWindowTitle("Добавление компании")
            
        layout = QFormLayout()
        
        self.name_field = QLineEdit()
        layout.addRow("Название:", self.name_field)
        
        self.state_field = QLineEdit()
        layout.addRow("Страна:", self.state_field)
        
        buttons = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow("", buttons)
        
        self.setLayout(layout)
        
        # Если редактируем существующую компанию, заполняем поля
        if self.company:
            self.name_field.setText(self.company['name'])
            self.state_field.setText(self.company['state'])
            
    def save(self):
        name = self.name_field.text()
        state = self.state_field.text()
        
        if not all([name, state]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
            
        if self.company:
            # Обновляем существующую компанию
            self.db.update_company(self.company['id'], name, state)
        else:
            # Добавляем новую компанию
            self.db.add_company(name, state)
            
        self.accept()


class PupDialog(QDialog):
    def __init__(self, parent, db, pup=None):
        super().__init__(parent)
        self.db = db
        self.pup = pup
        self.init_ui()
        
    def init_ui(self):
        if self.pup:
            self.setWindowTitle("Редактирование пункта выдачи")
        else:
            self.setWindowTitle("Добавление пункта выдачи")
            
        layout = QFormLayout()
        
        self.address_field = QLineEdit()
        layout.addRow("Адрес:", self.address_field)
        
        buttons = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow("", buttons)
        
        self.setLayout(layout)
        
        # Если редактируем существующий пункт выдачи, заполняем поля
        if self.pup:
            self.address_field.setText(self.pup['address'])
            
    def save(self):
        address = self.address_field.text()
        
        if not address:
            QMessageBox.warning(self, "Ошибка", "Введите адрес пункта выдачи")
            return
            
        if self.pup:
            # Обновляем существующий пункт выдачи
            self.db.update_pup(self.pup['id'], address)
        else:
            # Добавляем новый пункт выдачи
            self.db.add_pup(address)
            
        self.accept()