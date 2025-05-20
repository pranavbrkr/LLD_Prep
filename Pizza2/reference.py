from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List

# ------------------------
# Core Interfaces
# ------------------------

class MenuItem(ABC):
    @abstractmethod
    def get_price(self) -> Decimal:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

# ------------------------
# Base Pizza and Ingredients
# ------------------------

class PizzaBase(MenuItem):
    def __init__(self, name: str, price: Decimal):
        self.name = name
        self.price = price

    def get_price(self) -> Decimal:
        return self.price

    def get_description(self) -> str:
        return self.name

class Sauce(MenuItem):
    def __init__(self, name: str, price: Decimal):
        self.name = name
        self.price = price

    def get_price(self) -> Decimal:
        return self.price

    def get_description(self) -> str:
        return self.name

class Topping(MenuItem):
    def __init__(self, name: str, price: Decimal):
        self.name = name
        self.price = price

    def get_price(self) -> Decimal:
        return self.price

    def get_description(self) -> str:
        return self.name

# ------------------------
# Pizza (Custom or Premade)
# ------------------------

class Pizza(MenuItem):
    def __init__(self, base: PizzaBase):
        self.base = base
        self.sauces: List[Sauce] = []
        self.toppings: List[Topping] = []

    def add_sauce(self, sauce: Sauce):
        self.sauces.append(sauce)

    def add_topping(self, topping: Topping):
        self.toppings.append(topping)

    def get_price(self) -> Decimal:
        total = self.base.get_price()
        total += sum(s.get_price() for s in self.sauces)
        total += sum(t.get_price() for t in self.toppings)
        return total

    def get_description(self) -> str:
        desc = [self.base.get_description()]
        if self.sauces:
            desc.append("Sauces: " + ", ".join(s.get_description() for s in self.sauces))
        if self.toppings:
            desc.append("Toppings: " + ", ".join(t.get_description() for t in self.toppings))
        return " | ".join(desc)

# ------------------------
# Other Menu Items
# ------------------------

class Drink(MenuItem):
    def __init__(self, name: str, price: Decimal):
        self.name = name
        self.price = price

    def get_price(self) -> Decimal:
        return self.price

    def get_description(self) -> str:
        return self.name

class Side(MenuItem):
    def __init__(self, name: str, price: Decimal):
        self.name = name
        self.price = price

    def get_price(self) -> Decimal:
        return self.price

    def get_description(self) -> str:
        return self.name

# ------------------------
# Order
# ------------------------

class Order:
    def __init__(self):
        self.items: List[MenuItem] = []

    def add_item(self, item: MenuItem):
        self.items.append(item)

    def calculate_total(self) -> Decimal:
        return sum(item.get_price() for item in self.items)

    def print_summary(self):
        print("Order Summary:")
        for item in self.items:
            print(f"- {item.get_description()} : ${item.get_price()}")
        print(f"Total: ${self.calculate_total()}")

# ------------------------
# Demo
# ------------------------

if __name__ == "__main__":
    # Ingredients
    plain = PizzaBase("Plain Base", Decimal("4.00"))
    cheese = PizzaBase("Cheese Base", Decimal("5.00"))
    tomato = Sauce("Tomato", Decimal("0.50"))
    mayo = Sauce("Mayo", Decimal("0.70"))
    pepperoni = Topping("Pepperoni", Decimal("1.50"))
    onions = Topping("Onions", Decimal("0.80"))

    # Build custom pizza
    pizza = Pizza(cheese)
    pizza.add_sauce(tomato)
    pizza.add_topping(pepperoni)
    pizza.add_topping(onions)

    # Add other items
    drink = Drink("Coke", Decimal("1.50"))
    side = Side("Garlic Bread", Decimal("2.50"))

    # Place order
    order = Order()
    order.add_item(pizza)
    order.add_item(drink)
    order.add_item(side)
    order.print_summary()
