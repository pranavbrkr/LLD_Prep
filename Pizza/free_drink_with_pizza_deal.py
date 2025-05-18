from decimal import Decimal
from .deal import Deal
from .pizza import Pizza
from .drink import Drink
from .order import Order

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