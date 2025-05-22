import sys
import db_logic
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                           QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, 
                           QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox,
                           QTabWidget, QDateEdit, QMessageBox, QListWidget, 
                           QListWidgetItem, QGroupBox)
from PyQt5.QtCore import Qt, QDate

class ShopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Инициализация базы данных
        self.dbm = db_logic.DatabaseManager()
        self.dbm.connect()
        
        # Инициализация корзины [id_prod, name, quantity, price]
        self.cart = []
        
        # Настройка основного окна
        self.setWindowTitle("Система управления магазином")
        self.setGeometry(100, 100, 900, 700)  # x, y, ширина, высота
        
        # Создание центрального виджета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создание основного макета
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Создание компонентов интерфейса
        self.create_ui_components()
        
    def create_ui_components(self):
        # Заголовок
        header_label = QLabel("Система управления магазином")
        header_label.setStyleSheet("font-size: 24pt; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(header_label)
        
        # Создание вкладок
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Первая вкладка - Покупка товаров
        self.create_purchase_tab()
        
        # Вторая вкладка - Отчет о продажах
        self.create_sales_report_tab()
        
    def create_purchase_tab(self):
        purchase_tab = QWidget()
        layout = QVBoxLayout(purchase_tab)
        
        # Блок выбора товара
        product_group = QGroupBox("Выбор товара")
        product_layout = QVBoxLayout()
        
        # Строка выбора товара
        product_row = QHBoxLayout()
        
        # Комбо-бокс для выбора товара
        product_label = QLabel("Товар:")
        self.product_combo = QComboBox()
        self.update_product_combo()

        product_row.addWidget(product_label)
        product_row.addWidget(self.product_combo, 1)
        
        # Количество товара
        quantity_label = QLabel("Количество:")
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(1000)
        self.product_combo.currentIndexChanged.connect(self.update_max_quantity)
        
        product_row.addWidget(quantity_label)
        product_row.addWidget(self.quantity_spin)
        
        # Обновляем максимальное значение при первом выборе
        self.update_max_quantity()
        
        # Цена за выбранное количество
        self.price_label = QLabel("Цена: 0.00 руб.")
        
        # При изменении количества или товара обновляем цену
        self.quantity_spin.valueChanged.connect(self.update_price_label)
        self.product_combo.currentIndexChanged.connect(self.update_price_label)
        
        # Кнопка добавления в корзину
        add_button = QPushButton("Добавить в корзину")
        add_button.clicked.connect(self.add_to_cart)
        
        product_layout.addLayout(product_row)
        product_layout.addWidget(self.price_label)
        product_layout.addWidget(add_button)
        
        product_group.setLayout(product_layout)
        layout.addWidget(product_group)
        
        # Корзина
        cart_group = QGroupBox("Корзина")
        cart_layout = QVBoxLayout()
        
        self.cart_list = QListWidget()
        
        # Общая сумма
        self.total_price_label = QLabel("Итого: 0.00 руб.")
        self.total_price_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        self.total_price_label.setAlignment(Qt.AlignRight)
        
        # Кнопки удаления и оформления заказа
        buttons_layout = QHBoxLayout()
        
        clear_button = QPushButton("Очистить корзину")
        clear_button.clicked.connect(self.clear_cart)
        
        remove_button = QPushButton("Удалить выбранный")
        remove_button.clicked.connect(self.remove_selected_from_cart)
        
        checkout_button = QPushButton("Оформить покупку")
        checkout_button.clicked.connect(self.process_purchase)
        checkout_button.setStyleSheet("background-color: #4CAF50; color: white;")
        
        buttons_layout.addWidget(clear_button)
        buttons_layout.addWidget(remove_button)
        buttons_layout.addWidget(checkout_button)
        
        cart_layout.addWidget(self.cart_list)
        cart_layout.addWidget(self.total_price_label)
        cart_layout.addLayout(buttons_layout)
        
        cart_group.setLayout(cart_layout)
        layout.addWidget(cart_group)
        
        self.tabs.addTab(purchase_tab, "Покупка товаров")
    
    def create_sales_report_tab(self):
        sales_tab = QWidget()
        layout = QVBoxLayout(sales_tab)
        
        # Выбор даты
        date_layout = QHBoxLayout()
        date_label = QLabel("Выберите дату:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        
        load_button = QPushButton("Загрузить отчет")
        load_button.clicked.connect(self.load_sales_report)
        
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        date_layout.addWidget(load_button)
        date_layout.addStretch(1)
        
        layout.addLayout(date_layout)
        
        # Таблица для отображения отчета
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(2)
        self.report_table.setHorizontalHeaderLabels(["Товар", "Количество проданных"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.report_table)
        
        # Общая выручка за день
        self.revenue_label = QLabel("Общая выручка за день: 0.00 руб.")
        self.revenue_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        self.revenue_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(self.revenue_label)
        
        self.tabs.addTab(sales_tab, "Отчет о продажах")
    
    def update_product_combo(self):
        """Обновляет выпадающий список товаров"""
        self.product_combo.clear()
        products = self.dbm.get_products()
        
        # Сохраняем данные о товарах в комбобоксе
        for product in products:
            # Формат: "Название товара (в наличии: X)"
            product_id, category, name, price, quantity = product
            self.product_combo.addItem(f"{name} (в наличии: {quantity})", 
                                     [product_id, name, price, quantity])
    
    def update_max_quantity(self):
        """Обновляет максимальное значение в спиннере в зависимости от наличия товара"""
        if self.product_combo.count() == 0:
            return
            
        current_data = self.product_combo.currentData()
        if current_data:
            max_quantity = current_data[3]  # quantity
            self.quantity_spin.setMaximum(max_quantity)
            self.quantity_spin.setValue(1)  # Сбрасываем на 1 при смене товара
    
    def update_price_label(self):
        """Обновляет метку с ценой за выбранное количество товара"""
        if self.product_combo.count() == 0:
            return
            
        current_data = self.product_combo.currentData()
        if current_data:
            price = current_data[2]  # price в копейках
            quantity = self.quantity_spin.value()
            total = (price * quantity) / 100.0  # Перевод в рубли
            self.price_label.setText(f"Цена: {total:.2f} руб.")
    
    def add_to_cart(self):
        """Добавляет товар в корзину"""
        if self.product_combo.count() == 0:
            return
            
        current_data = self.product_combo.currentData()
        if current_data:
            product_id, name, price, available_quantity = current_data
            quantity = self.quantity_spin.value()
            
            # Проверка на достаточное количество товара
            if quantity > available_quantity:
                QMessageBox.warning(self, "Недостаточное количество", 
                                  f"В наличии только {available_quantity} единиц товара.")
                return
            
            # Проверяем, есть ли этот товар уже в корзине
            for i, item in enumerate(self.cart):
                if item[0] == product_id:
                    # Проверяем, не превысит ли суммарное количество доступное
                    total_quantity = item[2] + quantity
                    if total_quantity > available_quantity:
                        QMessageBox.warning(self, "Недостаточное количество", 
                                         f"В наличии только {available_quantity} единиц товара. "
                                         f"В корзине уже есть {item[2]} единиц.")
                        return
                    
                    # Обновляем количество и цену в существующей позиции
                    self.cart[i][2] = total_quantity
                    self.cart[i][3] = price * total_quantity
                    self.update_cart_display()
                    return
            
            # Если товара еще нет в корзине, добавляем новый элемент
            item_price = price * quantity
            self.cart.append([product_id, name, quantity, item_price])
            self.update_cart_display()
    
    def update_cart_display(self):
        """Обновляет отображение корзины и общую сумму"""
        self.cart_list.clear()
        total = 0
        
        for item in self.cart:
            product_id, name, quantity, price = item
            price_rub = price / 100.0
            self.cart_list.addItem(f"{name} - {quantity} шт. - {price_rub:.2f} руб.")
            total += price
        
        # Обновляем общую сумму
        self.total_price_label.setText(f"Итого: {total/100.0:.2f} руб.")
    
    def clear_cart(self):
        """Очищает корзину"""
        self.cart = []
        self.update_cart_display()
    
    def remove_selected_from_cart(self):
        """Удаляет выбранный товар из корзины"""
        selected_items = self.cart_list.selectedItems()
        if not selected_items:
            return
        
        # Получаем индекс выбранного элемента
        index = self.cart_list.row(selected_items[0])
        if 0 <= index < len(self.cart):
            del self.cart[index]
            self.update_cart_display()
    
    def process_purchase(self):
        """Обрабатывает покупку"""
        if not self.cart:
            QMessageBox.information(self, "Пустая корзина", "Добавьте товары в корзину перед оформлением покупки.")
            return
        
        try:
            # Форматируем данные для БД
            products = []
            total_price = 0
            
            for item in self.cart:
                product_id, _, quantity, price = item
                products.append((product_id, quantity, price))
                total_price += price
            
            # Текущая дата и время
            now = datetime.now()
            date_str = now.strftime('%Y-%m-%d %H:%M:%S')
            
            # Добавляем покупку в БД
            receipt_id = self.dbm.buy_products(products, date_str, total_price)
            
            QMessageBox.information(self, "Покупка оформлена", 
                                  f"Покупка успешно оформлена\nНомер чека: {receipt_id}")
            
            # Очищаем корзину и обновляем список товаров после покупки
            self.clear_cart()
            self.update_product_combo()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"При оформлении покупки произошла ошибка: {str(e)}")
    
    def load_sales_report(self):
        """Загружает отчет о продажах за выбранную дату"""
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        
        try:
            # Загрузка данных о продажах
            sales = self.dbm.get_goods(selected_date)
            
            # Настройка таблицы
            self.report_table.clearContents()
            self.report_table.setRowCount(len(sales))
            
            # Заполнение таблицы данными
            for row, sale in enumerate(sales):
                product_name, quantity = sale
                self.report_table.setItem(row, 0, QTableWidgetItem(product_name))
                self.report_table.setItem(row, 1, QTableWidgetItem(str(quantity)))
            
            # Запрашиваем общую выручку за день
            try:
                revenue_data = self.dbm.get_solds(selected_date)
                if revenue_data and len(revenue_data) > 0:
                    total_revenue = revenue_data[0][0] / 100.0  # Переводим из копеек в рубли
                    self.revenue_label.setText(f"Общая выручка за день: {total_revenue:.2f} руб.")
                else:
                    self.revenue_label.setText(f"Общая выручка за день: 0.00 руб.")
            except Exception as e:
                self.revenue_label.setText(f"Ошибка при загрузке выручки: {str(e)}")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"При загрузке отчета произошла ошибка: {str(e)}")
    
    def closeEvent(self, event):
        """Обработчик события закрытия окна"""
        # Закрываем соединение с БД при закрытии окна
        self.dbm.close()
        event.accept()