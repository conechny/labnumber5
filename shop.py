import sqlite3
from abc import ABC, abstractmethod

DB_NAME = "shop.db"

# Инициализация БД
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            product_price REAL
        )
    """)
    conn.commit()
    conn.close()

class Product(ABC):
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @abstractmethod
    def get_info(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

class Book(Product):
    def __init__(self, name, price, author):
        super().__init__(name, price)
        self.__author = author

    def get_info(self):
        return f"Книга: {self.name}, Автор: {self.__author}, Цена: {self.price} руб."

class Laptop(Product):
    def __init__(self, name, price, brand):
        super().__init__(name, price)
        self.__brand = brand

    def get_info(self):
        return f"Ноутбук: {self.name}, Бренд: {self.__brand}, Цена: {self.price} руб."

class User:
    def __init__(self):
        self.balance = 0
        self.cart = []

    def add_to_cart(self, product):
        self.cart.append(product)

    def show_cart(self):
        if not self.cart:
            print("Корзина пуста.")
            return
        for i, item in enumerate(self.cart, 1):
            print(f"{i}. {item.get_info()}")

    def checkout(self):
        total = sum(item.price for item in self.cart)
        if total > self.balance:
            print("Недостаточно средств!")
            return
        self.balance -= total
        for item in self.cart:
            self.save_to_db(item)
        self.cart.clear()
        print("Покупка успешно оформлена!")

    def add_balance(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Счет пополнен на {amount} руб. Текущий баланс: {self.balance} руб.")

    def show_history(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, product_price FROM purchase_history")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            print("История покупок пуста.")
            return
        for name, price in rows:
            print(f"{name} - {price} руб.")

    def save_to_db(self, product):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO purchase_history (product_name, product_price) VALUES (?, ?)",
            (product.name, product.price)
        )
        conn.commit()
        conn.close()

def main():
    init_db()
    user = User()
    categories = {
        "Книги": [Book("1984", 500, "Джордж Оруэлл"), Book("Мастер и Маргарита", 600, "Булгаков")],
        "Ноутбуки": [Laptop("MacBook Air", 95000, "Apple"), Laptop("Aspire 5", 45000, "Acer")]
    }

    while True:
        print("\nДобро пожаловать. Выберите действие:")
        print("1. Посмотреть категории")
        print("2. Перейти в корзину")
        print("3. Перейти в историю покупок")
        print("4. Посмотреть счет")
        print("5. Пополнить счет")
        print("0. Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            cat_choice = int(input("Выберите категорию: ")) - 1
            cat_keys = list(categories.keys())
            if 0 <= cat_choice < len(cat_keys):
                products = categories[cat_keys[cat_choice]]
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product.get_info()}")
                prod_choice = int(input("Выберите товар для добавления в корзину: ")) - 1
                if 0 <= prod_choice < len(products):
                    user.add_to_cart(products[prod_choice])
                    print("Товар добавлен в корзину.")
        elif choice == "2":
            user.show_cart()
            sub = input("Хотите оформить покупку? (да/нет): ")
            if sub.lower() == "да":
                user.checkout()
        elif choice == "3":
            user.show_history()
        elif choice == "4":
            print(f"Ваш текущий счет: {user.balance} руб.")
        elif choice == "5":
            amt = float(input("Введите сумму пополнения: "))
            user.add_balance(amt)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()
