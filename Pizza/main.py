from decimal import Decimal
from .store import Store
from .order import Order
from .buy_one_get_one_free_pizza_deal import BuyOneGetOneFreePizzaDeal
from .free_drink_with_pizza_deal import FreeDrinkWithPizzaDeal
from .most_expensive_topping_free_deal import MostExpensiveToppingFreeDeal

def main():
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

if __name__ == "__main__":
  main()