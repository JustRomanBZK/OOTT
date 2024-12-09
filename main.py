from enum import Enum
from datetime import date
from typing import List


class UserRole(Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    MANAGER = "MANAGER"
    WAREHOUSE_WORKER = "WAREHOUSE_WORKER"
    CASHIER = "CASHIER"
    CUSTOMER = "CUSTOMER"


class User:
    def __init__(self, user_id: int, name: str, login: str, password: str, role: UserRole):
        self.id = user_id
        self.name = name
        self.login = login
        self.password = password
        self.role = role

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, role={self.role.value})"


class Category:
    def __init__(self, category_id: int, name: str):
        self.id = category_id
        self.name = name

    def __str__(self):
        return f"Category(id={self.id}, name={self.name})"


class Product:
    def __init__(self, product_id: int, name: str, price: float, category: Category):
        self.id = product_id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, category={self.category.name})"


class Supplier:
    def __init__(self, supplier_id: int, name: str):
        self.id = supplier_id
        self.name = name
        self._provided_products: List[Product] = []

    def add_product(self, product: Product):
        self._provided_products.append(product)

    def get_provided_products(self) -> List[Product]:
        return self._provided_products

    def __str__(self):
        return f"Supplier(id={self.id}, name={self.name})"


class WarehouseCell:
    def __init__(self, cell_id: int, location: str, capacity: int):
        self.id = cell_id
        self.location = location
        self.capacity = capacity

    def __str__(self):
        return f"WarehouseCell(id={self.id}, location={self.location}, capacity={self.capacity})"


class InventoryRecord:
    def __init__(self, record_id: int, product: Product, cell: WarehouseCell, quantity: int):
        self.id = record_id
        self.product = product
        self.cell = cell
        self.quantity = quantity

    def get_available_quantity(self) -> int:
        return self.quantity
    def report_defect(self, qty: int):
        if qty <= self.quantity:
            self.quantity -= qty
        else:
            raise("Нема стільки товару.")

    def __str__(self):
        return f"InventoryRecord(id={self.id}, product={self.product.name}, cell={self.cell.location}, qty={self.quantity})"


class OrderLine:
    def __init__(self, line_id: int, product: Product, quantity: int, unit_price: float):
        self.id = line_id
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price

    def get_line_total(self) -> float:
        return self.quantity * self.unit_price

    def __str__(self):
        return f"OrderLine(id={self.id}, product={self.product.name}, qty={self.quantity}, unit_price={self.unit_price})"



class Address:
    def __init__(self, country: str, city: str, street: str):
        self.country = country
        self.city = city
        self.street = street

class Customer:
    def __init__(self, customer_id: int, name: str, contact_info: str, address: Address = None):
        self.id = customer_id
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"Customer(id={self.id}, name={self.name}, contact={self.contact_info})"

class CustomerOrder:
    def __init__(self, order_id: int, customer: Customer, date_: date, status: str):
        self.id = order_id
        self.customer = customer
        self.date = date_
        self.status = status
        self.order_lines: List[OrderLine] = []

    def add_order_line(self, line: OrderLine):
        self.order_lines.append(line)

    def get_total(self) -> float:
        return sum(line.get_line_total() for line in self.order_lines)

    def __str__(self):
        return f"CustomerOrder(id={self.id}, customer={self.customer.name}, total={self.get_total()})"



class Sale:
    def __init__(self, sale_id: int, date_: date, total_amount: float):
        self.id = sale_id
        self.date = date_
        self.total_amount = total_amount

    def print_receipt(self):
        print(f"Receipt: Sale ID={self.id}, Date={self.date}, Total={self.total_amount}")

    def __str__(self):
        return f"Sale(id={self.id}, date={self.date}, total={self.total_amount})"




if __name__ == "__main__":

    eng_category = Category(category_id=1, name="Engines")

    product1 = Product(product_id=101, name="Engine V6", price=2500.00, category=eng_category)
    product2 = Product(product_id=102, name="Engine V8", price=4000.00, category=eng_category)

    supplier = Supplier(supplier_id=201, name="Motors")
    supplier.add_product(product1)
    supplier.add_product(product2)

    cell = WarehouseCell(cell_id=301, location="A1", capacity=100)
    inv_record1 = InventoryRecord(record_id=401, product=product1, cell=cell, quantity=10)
    inv_record2 = InventoryRecord(record_id=402, product=product2, cell=cell, quantity=5)

    inv_record1.report_defect(2)

    adr = Address(
        country="Ukraine",
        city="Kyiv",
        street="Khreshchatyk"
    )
    customer = Customer(customer_id=501, name="Пан Роман", contact_info="pan@roman.com", address=adr)
    print(customer)

    order = CustomerOrder(order_id=601, customer=customer, date_=date.today(), status="Pending")


    print(product1.price, product2.price)
    order_line1 = OrderLine(line_id=701, product=product1, quantity=2, unit_price=product1.price)
    order_line2 = OrderLine(line_id=702, product=product2, quantity=1, unit_price=product2.price)

    order.add_order_line(order_line1)
    order.add_order_line(order_line2)

    print(order.get_total())


    sale = Sale(sale_id=801, date_=date.today(), total_amount=order.get_total())
    sale.print_receipt()

    manager = User(user_id=901, name="Manager1", login="manager1", password="pass", role=UserRole.MANAGER)
    print(manager)

    for p in supplier.get_provided_products():
        print(p)


    print(inv_record1)
    print(inv_record2)