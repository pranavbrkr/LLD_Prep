from decimal import Decimal
from typing import List
from .topping import Topping
from .base import Base
from .order_item import OrderItem

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