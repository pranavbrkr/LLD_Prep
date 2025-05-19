Define a abstract OrderItem class with name and price attributes
Define Base, Drink, Topping class which extend this abstract class


Pizza class: extends OrderItemhas the base and list of toppings
attr: base_pizza, list(toppings)
methods: add topping, get toppings, get price

Catalog class: holds all the base prices, topping prices, drink prices
attr: base_prices, topping_prices, drink_prices .... (all dicts)
methods: add baseprice, topping price and drink prices, createBase, createTopping and createDrink

PizzaBuilder: class to construct Pizza
attr: catalog, base, toppings
methods: withBase, addTopping and build

Order class:
attr: items
methods: add item, get Items and calculate Subtotal

class Deal: abstract class to calculate Discount

class DiscountCalculator: 
contains deals and method to calculate discount(call to all calculateDiscount for all deals)

class FreeDrinkWithPizzaDeal: extends Deal
contains calculateDiscount method to calculate discount where cheapest drink is free


Store class:
contains name, catalog and deals
methods to add deal, get deal and buildPizza