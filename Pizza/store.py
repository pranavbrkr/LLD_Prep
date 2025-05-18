from decimal import Decimal
from typing import Dict, List
from .base import Base
from .topping import Topping
from .drink import Drink
from .deal import Deal

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
    from .pizza_builder import PizzaBuilder
    return PizzaBuilder(self)