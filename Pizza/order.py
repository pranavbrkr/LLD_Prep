from decimal import Decimal
from typing import List
from .order_item import OrderItem
from .store import Store

class Order:
  def __init__(self, store: Store):
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