from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List

class MenuItem(ABC):
  @abstractmethod
  def getPrice(self):
    pass

  @abstractmethod
  def getDescription(self):
    pass

class PizzaBase(MenuItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self):
    return self.price
  
  def getDescription(self):
    return self.name

class Sauce(MenuItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self):
    return self.price
  
  def getDescription(self):
    return self.name

class Topping(MenuItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self):
    return self.price
  
  def getDescription(self):
    return self.name


class Pizza(MenuItem):
  def __init__(self, base: PizzaBase):
    self.base = base
    self.sauces: List[Sauce] = []
    self.toppings: List[Topping] = []
  
  def addSauce(self, sauce: Sauce):
    self.sauces.append(sauce)
  
  def addTopping(self, topping: Topping):
    self.toppings.append(topping)
  
  def getPrice(self):
    total = self.base.getPrice()
    total += sum(s.getPrice() for s in self.sauces)
    total += sum(t.getPrice() for t in self.toppings)
    return total

  def getDescription(self):
    desc = [self.base.getDescription()]
    if self.sauces:
      desc.append("Sauces: " + ", ".join(s.getDescription() for s in self.sauces))
    if self.toppings:
      desc.append("Toppings: " + ", ".join(t.getDescription() for t in self.toppings))
    return " | ".join(desc)

class Drink(MenuItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self):
    return self.price
  
  def getDescription(self):
    return self.name

class Side(MenuItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self):
    return self.price
  
  def getDescription(self):
    return self.name

class Order:
  def __init__(self):
    self.items: List[MenuItem] = []
  
  def addItem(self, item: MenuItem):
    self.items.append(item)

  def calculateTotal(self):
    return sum(item.getPrice() for item in self.items)

  def printSummary(self):
    print("Order summary:")
    for item in self.items:
      print(f"- {item.getDescription()}: ${item.getPrice()}")
    print(f"Total: ${self.calculateTotal()}")
  

if __name__ == "__main__":
  plain = PizzaBase("Plain Base", Decimal("4.00"))
  cheese = PizzaBase("Cheese Base", Decimal("5.00"))
  tomato = Sauce("Tomato", Decimal("0.50"))
  mayo = Sauce("Mayo", Decimal("0.70"))
  pepperoni = Topping("Pepperoni", Decimal("1.50"))
  onions = Topping("Onions", Decimal("0.80"))

  pizza = Pizza(cheese)
  pizza.addSauce(tomato)
  pizza.addTopping(pepperoni)
  pizza.addTopping(onions)

  drink = Drink("Coke", Decimal("1.50"))
  side = Side("Garlic Bread", Decimal("2.50"))

  order = Order()
  order.addItem(pizza)
  order.addItem(drink)
  order.addItem(side)
  order.printSummary()