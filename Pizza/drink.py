from decimal import Decimal
from .order_item import OrderItem

class Drink(OrderItem):
  def __init__(self, name: str, price: Decimal):
    self.name = name
    self.price = price
  
  def getPrice(self) -> Decimal:
    return self.price