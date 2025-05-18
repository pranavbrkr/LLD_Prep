from decimal import Decimal
from .deal import Deal
from .pizza import Pizza
from .topping import Topping
from .order import Order
from .order_item import OrderItem

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