
# ---------------- enums.py ----------------
from enum import Enum

class Coin(Enum):
  PENNY = 0.01
  NICKEL = 0.05
  DIME = 0.1
  QUARTER = 0.25

class Note(Enum):
  ONE = 1
  FIVE = 5
  TEN = 10
  TWENTY = 20

# ---------------- product.py ----------------
class Product:
  def __init__(self, name, price):
    self._name = name
    self._price = price

  def getName(self):
    return self._name

  def getPrice(self):
    return self._price

# ---------------- inventory.py ----------------
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

# ---------------- vending_machine_state.py ----------------
from abc import ABC, abstractmethod

class VendingMachineState(ABC):
  def __init__(self, vending_machine):
    self.vending_machine = vending_machine

  @abstractmethod
  def selectProduct(self, product):
    pass

  @abstractmethod
  def insertCoin(self, coin):
    pass

  @abstractmethod
  def insertNote(self, note):
    pass

  @abstractmethod
  def cancelTransaction(self):
    pass

  @abstractmethod
  def dispenseProduct(self):
    pass

  @abstractmethod
  def returnChange(self):
    pass

# ---------------- idle_state.py ----------------
class IdleState(VendingMachineState):
  def selectProduct(self, product):
    if self.vending_machine.inventory.isAvailable(product):
      self.vending_machine.selected_product = product
      print(f'Product selected: {product.getName()}')
      self.vending_machine.setState(self.vending_machine.ready_state)
    else:
      print(f"Product not available: {product.name}")

  def insertCoin(self, coin):
    print("Please select a product first")

  def insertNote(self, note):
    print("Please select a product first")

  def cancelTransaction(self):
    print("No transaction to cancel at this stage.")

  def dispenseProduct(self):
    print("Please select a product first")

  def returnChange(self):
    print("No change to return")

# ---------------- ready_state.py ----------------
class ReadyState(VendingMachineState):
  def selectProduct(self, product):
    print("Product already selected. Please make payment")

  def insertCoin(self, coin):
    self.vending_machine.addCoin(coin)
    print(f"Coin inserted: ${coin.value}")
    self.checkPaymentStatus()

  def insertNote(self, note):
    self.vending_machine.addNote(note)
    print(f"Note inserted: ${note.value}")
    self.checkPaymentStatus()

  def cancelTransaction(self):
    inserted = self.vending_machine.inserted_money
    if inserted:
      print(f"Transaction cancelled. Returning")
      for denom, count in inserted.items():
        print(f"${denom.value}: {count}")
    else:
      print("Transaction cancelled. No payment to return")
    self.vending_machine.resetPayment()
    self.vending_machine.resetSelectedProduct()
    self.vending_machine.setState(self.vending_machine.idle_state)

  def dispenseProduct(self):
    print("Please make payment first")

  def returnChange(self):
    print("Please make payment first")

  def checkPaymentStatus(self):
    if self.vending_machine.getTotalPayment() >= self.vending_machine.selected_product.getPrice():
      self.vending_machine.setState(self.vending_machine.dispense_state)

# ---------------- dispense_state.py ----------------
class DispenseState(VendingMachineState):
  def selectProduct(self, product):
    print("Product already selected. Please collect the dispensed product")

  def insertCoin(self, coin):
    print("Payment already made. Please collect the dispensed product")

  def insertNote(self, note):
    print("Payment already made. Please collect the dispensed product")

  def cancelTransaction(self):
    print("No transaction to cancel at this stage.")

  def dispenseProduct(self):
    product = self.vending_machine.selected_product
    self.vending_machine.inventory.updateQuantity(product, self.vending_machine.inventory.getQuantity(product) - 1)
    print(f"Product dispensed: {product.getName()}")
    self.vending_machine.setState(self.vending_machine.return_change_state)

  def returnChange(self):
    print("Please collect the dispensed product first")

# ---------------- return_change_state.py ----------------
class ReturnChangeState(VendingMachineState):
  def selectProduct(self, product):
    print("Please collect the change first")

  def insertCoin(self, coin):
    print("Please collect the change first")

  def insertNote(self, note):
    print("Please collect the change first")

  def cancelTransaction(self):
    print("No transaction to cancel at this stage.")

  def dispenseProduct(self):
    print("Product already dispensed. Please collect the change")

  def returnChange(self):
    change = self.vending_machine.getTotalPayment() - self.vending_machine.selected_product.getPrice()
    change_map = self.vending_machine.calculateChange(change)
    if change_map:
      print(f"Change returned:")
      for denom, count in change_map.items():
        print(f"${denom.value}: {count}")
    else:
      print("No change to return")
    self.vending_machine.resetPayment()
    self.vending_machine.resetSelectedProduct()
    self.vending_machine.setState(self.vending_machine.idle_state)

# ---------------- vending_machine.py ----------------
from threading import Lock

class VendingMachine:
  _instance = None
  _lock = Lock()

  def __new__(cls):
    with cls._lock:
      if cls._instance is None:
        cls._instance = super().__new__(cls)
        cls._instance._initialize()
    return cls._instance

  def _initialize(self):
    self.inventory = Inventory()
    self.idle_state = IdleState(self)
    self.ready_state = ReadyState(self)
    self.dispense_state = DispenseState(self)
    self.return_change_state = ReturnChangeState(self)
    self.current_state = self.idle_state
    self.selected_product = None
    self.inserted_money = {}
    self.total_payment = 0.0

  @classmethod
  def getInstance(cls):
    return cls()

  def selectProduct(self, product):
    self.current_state.selectProduct(product)

  def insertCoin(self, coin):
    self.current_state.insertCoin(coin)

  def insertNote(self, note):
    self.current_state.insertNote(note)

  def dispenseProduct(self):
    self.current_state.dispenseProduct()

  def returnChange(self):
    self.current_state.returnChange()

  def setState(self, state):
    self.current_state = state

  def addCoin(self, coin):
    self.inserted_money[coin] = self.inserted_money.get(coin, 0) + 1

  def addNote(self, note):
    self.inserted_money[note] = self.inserted_money.get(note, 0) + 1

  def cancelTransaction(self):
    self.current_state.cancelTransaction()

  def getTotalPayment(self):
    return sum(k.value * v for k, v in self.inserted_money.items())

  def calculateChange(self, amount):
    change_map = {}
    denominations = list(Note) + list(Coin)
    denominations.sort(key=lambda d: d.value, reverse=True)

    remaining = round(amount, 2)

    for denom in denominations:
      count = int(remaining // denom.value)
      if count > 0:
        change_map[denom] = count
        remaining -= round(denom.value * count, 2)

    return change_map

  def resetPayment(self):
    self.inserted_money.clear()

  def resetSelectedProduct(self):
    self.selected_product = None

# ---------------- main.py ----------------
if __name__ == "__main__":
  vending_machine = VendingMachine.getInstance()

  coke = Product("Coke", 1.5)
  pepsi = Product("Pepsi", 1.5)
  water = Product("Water", 1.5)

  vending_machine.inventory.addProduct(coke, 5)
  vending_machine.inventory.addProduct(pepsi, 3)
  vending_machine.inventory.addProduct(water, 2)

  vending_machine.selectProduct(coke)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.insertNote(Note.FIVE)
  vending_machine.dispenseProduct()
  vending_machine.returnChange()

  print("####################")

  vending_machine.selectProduct(pepsi)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.dispenseProduct()
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.dispenseProduct()
  vending_machine.returnChange()

  print("####################")

  vending_machine.selectProduct(coke)
  vending_machine.insertCoin(Coin.QUARTER)
  vending_machine.cancelTransaction()
