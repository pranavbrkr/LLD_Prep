from decimal import Decimal
from .deal import Deal
from .pizza import Pizza
from .order import Order

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