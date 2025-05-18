from typing import List
from .base import Base
from .topping import Topping
from .pizza import Pizza
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from store import Store

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