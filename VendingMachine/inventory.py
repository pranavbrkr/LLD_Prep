class Inventory:
  def __init__(self):
    self._products = {}

  def addProduct(self, product, quantity):
    self._products[product] = self._products.get(product, 0) + quantity
  
  def removeProduct(self, product):
    del self._products[product]
  
  def getQuantity(self, product):
    return self._products.get(product, 0)
  
  def updateQuantity(self, product, quantity):
    self._products[product] = quantity

  def isAvailable(self, product):
    return product in self._products and self._products[product] > 0