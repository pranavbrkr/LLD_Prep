from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Dict

# -----------------------------
# Domain Models
# -----------------------------

class OrderItem(ABC):
  @abstractmethod
  def getPrice(self) -> Decimal:
    pass

class Base(OrderItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price

  def getPrice(self) -> Decimal:
    return self.price

class Drink(OrderItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self) -> Decimal:
    return self.price

class Topping(OrderItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price

  def getPrice(self) -> Decimal:
    return self.price

class Pizza(OrderItem):
  def __init__(self, pizza_base: Base):
    self.pizza_base = pizza_base
    self.toppings: List[Topping] = []

  def addTopping(self, topping: Topping) -> None:
    self.toppings.append(topping)

  def getToppings(self) -> List[Topping]:
    return self.toppings

  def getPrice(self) -> Decimal:
    return self.pizza_base.getPrice() + sum(t.getPrice() for t in self.toppings)


# -----------------------------
# Catalog for Price and Creation
# -----------------------------

class Catalog:
  def __init__(self):
    self.base_prices: Dict[str, Decimal] = {}
    self.topping_prices: Dict[str, Decimal] = {}
    self.drink_prices: Dict[str, Decimal] = {}

  def addBasePrice(self, name: str, price: Decimal):
    self.base_prices[name] = price

  def addToppingPrice(self, name: str, price: Decimal):
    self.topping_prices[name] = price

  def addDrinkPrice(self, name: str, price: Decimal):
    self.drink_prices[name] = price

  def createBase(self, name: str) -> Base:
    return Base(name, self.base_prices[name])

  def createTopping(self, name: str) -> Topping:
    return Topping(name, self.topping_prices[name])

  def createDrink(self, name: str) -> Drink:
    return Drink(name, self.drink_prices[name])


# -----------------------------
# Builder for Pizza
# -----------------------------

class PizzaBuilder:
  def __init__(self, catalog: Catalog):
    self.catalog = catalog
    self.base: Base = None
    self.toppings: List[Topping] = []

  def withBase(self, base_name: str) -> 'PizzaBuilder':
    self.base = self.catalog.createBase(base_name)
    return self

  def addTopping(self, topping_name: str) -> 'PizzaBuilder':
    self.toppings.append(self.catalog.createTopping(topping_name))
    return self

  def build(self) -> Pizza:
    if not self.base:
      raise ValueError("Pizza base must be selected")
    pizza = Pizza(self.base)
    for topping in self.toppings:
      pizza.addTopping(topping)
    return pizza


# -----------------------------
# Order and Discount Engine
# -----------------------------

class Order:
  def __init__(self):
    self.items: List[OrderItem] = []

  def addItem(self, item: OrderItem):
    self.items.append(item)

  def getItems(self) -> List[OrderItem]:
    return self.items.copy()

  def calculateSubtotal(self) -> Decimal:
    return sum(item.getPrice() for item in self.items)


class Deal(ABC):
  @abstractmethod
  def calculateDiscount(self, order: Order) -> Decimal:
    pass

class DiscountCalculator:
  def __init__(self, deals: List[Deal]):
    self.deals = deals

  def calculate(self, order: Order) -> Decimal:
    return sum(deal.calculateDiscount(order) for deal in self.deals)

class BuyOneGetOneFreePizzaDeal(Deal):
  def calculateDiscount(self, order: Order) -> Decimal:
    pizzas = sorted(
      [item for item in order.getItems() if isinstance(item, Pizza)],
      key=lambda p: p.getPrice()
    )
    discount = sum(pizzas[i * 2].getPrice() for i in range(len(pizzas) // 2))
    return discount

class FreeDrinkWithPizzaDeal(Deal):
  def calculateDiscount(self, order: Order) -> Decimal:
    if not any(isinstance(item, Pizza) for item in order.getItems()):
      return Decimal("0.00")
    drinks = [item for item in order.getItems() if isinstance(item, Drink)]
    if not drinks:
      return Decimal("0.00")
    return min(drinks, key=lambda d: d.getPrice()).getPrice()

class MostExpensiveToppingFreeDeal(Deal):
  def calculateDiscount(self, order: Order) -> Decimal:
    discount = Decimal("0.00")
    for item in order.getItems():
      if isinstance(item, Pizza):
        toppings = item.getToppings()
        if toppings:
          discount += max(toppings, key=lambda t: t.getPrice()).getPrice()
    return discount


# -----------------------------
# Store (Business Rules)
# -----------------------------

class Store:
  def __init__(self, name: str, catalog: Catalog):
    self.name = name
    self.catalog = catalog
    self.deals: List[Deal] = []

  def addDeal(self, deal: Deal):
    self.deals.append(deal)

  def getDeals(self) -> List[Deal]:
    return self.deals.copy()

  def buildPizza(self) -> PizzaBuilder:
    return PizzaBuilder(self.catalog)


# -----------------------------
# Demo
# -----------------------------

if __name__ == "__main__":
  catalog = Catalog()
  catalog.addBasePrice("Thin Crust", Decimal("5.0"))
  catalog.addToppingPrice("Cheese", Decimal("1.0"))
  catalog.addToppingPrice("Pepperoni", Decimal("2.0"))
  catalog.addDrinkPrice("Cola", Decimal("3.0"))

  store = Store("Tempe", catalog)
  store.addDeal(BuyOneGetOneFreePizzaDeal())
  store.addDeal(FreeDrinkWithPizzaDeal())
  store.addDeal(MostExpensiveToppingFreeDeal())

  pizza1 = store.buildPizza().withBase("Thin Crust").addTopping("Cheese").addTopping("Pepperoni").build()
  pizza2 = store.buildPizza().withBase("Thin Crust").addTopping("Cheese").build()
  cola = catalog.createDrink("Cola")

  order = Order()
  order.addItem(pizza1)
  order.addItem(pizza2)
  order.addItem(cola)

  subtotal = order.calculateSubtotal()
  discount_calculator = DiscountCalculator(store.getDeals())
  discounts = discount_calculator.calculate(order)
  total = subtotal - discounts

  print("--------------------")
  print(f"Subtotal: {subtotal}")
  print(f"Discounts: {discounts}")
  print(f"Total: {total}")
