Firstly
We define abstract OrderItem class, with name and price
Define Topping, Base, Drink which extend this OrderItem class

Define Pizza class which also extends this OrderItem class
This has pizza_base, and list of toppings
And methods to add toppings and get price


Catalog class has dictionaries of base prices, topping prices and drink prices
And methods to create new of those items or add some price to existing 

Now
We have PizzaBuilder class
this has catalog, base and list of toppings
And following behaviors
withBase() returns self with createBase call to catalog
addTopping to add toppings to self and return it
build() creates a Pizza object with the base and adds toppings to that pizza and returns it


Then you have order class that contains list of items and methods to calculate subtotal


Then for discounts

We define one abstract Deal class with calculateDiscount(order)