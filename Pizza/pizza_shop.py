from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Dict

# Order Item ABC
class OrderItem(ABC):
  @abstractmethod
  def getPrice(self) -> Decimal:
    pass

# Base Pizza
class Base(OrderItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self) -> Decimal:
    return self.price

# Drink
class Drink(OrderItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self) -> Decimal:
    return self.price
  
# Topping
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
    total_price = self.pizza_base.getPrice()
    for topping in self.toppings:
      total_price += topping.getPrice()
    return total_price


class Order:
  def __init__(self, store):
    self.store: Store = store
    self.items: List[OrderItem] = []
  
  def getItems(self) -> List[OrderItem]:
    return self.items.copy()

  def addItem(self, item: OrderItem):
    self.items.append(item)
  
  def calculateTotal(self) -> Decimal:
    sub_total = sum(item.getPrice() for item in self.items)
    discounts = sum(deal.calculateDiscount(self) for deal in self.store.getDeals())

    print("--------------------")
    print(f"SubTotal: {sub_total}")
    print(f"Discounts: {discounts}")

    return sub_total - discounts

class Deal(ABC):
  @abstractmethod
  def calculateDiscount(self, order) -> Decimal:
    pass


class BuyOneGetOneFreePizzaDeal(Deal):
  def calculateDiscount(self, order: Order) -> Decimal:
    pizzas = sorted(
      [item for item in order.getItems() if isinstance(item, Pizza)],
      key = lambda p: p.getPrice()
    )

    pairs = len(pizzas) // 2
    discount = Decimal('0.00')

    for i in range(pairs):
      discount += pizzas[i * 2].getPrice()
    
    print(f"Discount for BuyOneGetOneFreePizzaDeal: {discount}")
    return discount

class FreeDrinkWithPizzaDeal(Deal):
  def calculateDiscount(self, order: Order) -> Decimal:
    has_pizza = any(isinstance(item, Pizza) for item in order.getItems())
    if not has_pizza:
      return Decimal('0.00')
    
    drinks = [item for item in order.getItems() if isinstance(item, Drink)]
    if not drinks:
      return Decimal('0.00')
    
    cheapest_drink = min(drinks, key=lambda d: d.getPrice())
    discount = cheapest_drink.getPrice()

    print(f"Discount for FreeDrinkWithPizzaDeal: {discount}")
    return discount

class MostExpensiveToppingFreeDeal(Deal):
  def calculateDiscount(self, order: Order) -> Decimal:
    total_discount = Decimal('0.00')
    for item in order.getItems():
      if isinstance(item, Pizza):
        toppings = item.getToppings()
        if toppings:
          most_expensive = max(toppings, key=lambda t:t.getPrice(), default=None)
          if most_expensive:
            total_discount += most_expensive.getPrice()
    
    print(f"Discount for MostExpensiveToppingFreeDeal: {total_discount}")
    return total_discount


class PizzaBuilder:
  def __init__(self, store: 'Store'):
    self.store = store
    self.base: Base = None
    self.toppings: List[Topping] = []
  
  def withBase(self, base_name: str) -> 'PizzaBuilder':
    self.base = self.store.createBase(base_name)
    return self
  
  def addTopping(self, topping_name: str) -> 'PizzaBuilder':
    topping = self.store.createTopping(topping_name)
    self.toppings.append(topping)
    return self

  def build(self) -> Pizza:
    if self.base is None:
      raise ValueError("Pizza base must be selected")
    
    pizza = Pizza(self.base)
    for topping in self.toppings:
      pizza.addTopping(topping)
    return pizza

class Store:
  def __init__(self, name: str):
    self.name = name
    self.base_prices: Dict[str, Decimal] = {}
    self.topping_prices: Dict[str, Decimal] = {}
    self.drink_prices: Dict[str, Decimal] = {}
    self.deals: List[Deal] = []
  
  def addBasePrice(self, name:str, price: Decimal) -> None:
    self.base_prices[name] = price
  
  def addToppingPrice(self, name:str, price: Decimal) -> None:
    self.topping_prices[name] = price
  
  def addDrinkPrice(self, name:str, price: Decimal) -> None:
    self.drink_prices[name] = price
  
  def addDeal(self, deal: Deal):
    self.deals.append(deal)
  
  def createBase(self, name: str) -> Base:
    if name not in self.base_prices:
      raise ValueError(f"Base '{name}' not found in store price list")
    return Base(name, self.base_prices[name])
  
  def createTopping(self, name: str) -> Base:
    if name not in self.topping_prices:
      raise ValueError(f"Topping '{name}' not found in store price list")
    return Topping(name, self.topping_prices[name])
  
  def createDrink(self, name: str) -> Base:
    if name not in self.drink_prices:
      raise ValueError(f"Drink '{name}' not found in store price list")
    return Topping(name, self.drink_prices[name])
  
  def getDeals(self) -> List[Deal]:
    return self.deals.copy()
  
  def buildPizza(self) -> 'PizzaBuilder':
    return PizzaBuilder(self)


if __name__ == "__main__":
  tempe_store = Store("Tempe")
  tempe_store.addBasePrice("Thin Crust", Decimal("5.0"))
  tempe_store.addToppingPrice("Cheese", Decimal("1.0"))
  tempe_store.addToppingPrice("Pepperoni", Decimal("2.0"))
  tempe_store.addDrinkPrice("Cola", Decimal("3.0"))

  tempe_store.addDeal(BuyOneGetOneFreePizzaDeal())
  tempe_store.addDeal(FreeDrinkWithPizzaDeal())
  tempe_store.addDeal(MostExpensiveToppingFreeDeal())

  thin_crust_cheese_pepperoni_pizza = tempe_store.buildPizza()\
                                      .withBase("Thin Crust")\
                                      .addTopping("Cheese")\
                                      .addTopping("Pepperoni")\
                                      .build()

  thin_crust_cheese_pizza = tempe_store.buildPizza()\
                            .withBase("Thin Crust")\
                            .addTopping("Cheese")\
                            .build()
  
  cola = tempe_store.createDrink("Cola")
  order = Order(tempe_store)
  order.addItem(thin_crust_cheese_pepperoni_pizza)
  order.addItem(thin_crust_cheese_pizza)
  order.addItem(cola)

  print("--------------------")
  print(f"Total Price: {order.calculateTotal()}")