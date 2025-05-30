from threading import Lock

from dispense_state import DispenseState
from enums import Coin, Note
from idle_state import IdleState
from inventory import Inventory
from product import Product
from ready_state import ReadyState
from return_change_state import ReturnChangeState
from vending_machine_state import VendingMachineState

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
    self.inventory: Inventory = Inventory()
    self.idle_state = IdleState(self)
    self.ready_state = ReadyState(self)
    self.dispense_state = DispenseState(self)
    self.return_change_state = ReturnChangeState(self)
    self.current_state = self.idle_state
    self.selected_product: Product = None
    self.inserted_money = {}
    self.total_payment = 0.0

  @classmethod
  def getInstance(cls):
    return cls()
  
  def selectProduct(self, product: Product):
    self.current_state.selectProduct(product)
  
  def insertCoin(self, coin: Coin):
    self.current_state.insertCoin(coin)
  
  def insertNote(self, note: Note):
    self.current_state.insertNote(note)
  
  def dispenseProduct(self):
    self.current_state.dispenseProduct()
  
  def returnChange(self):
    self.current_state.returnChange()
  
  def setState(self, state: VendingMachineState):
    self.current_state = state
  
  def addCoin(self, coin: Coin):
    self.inserted_money[coin] = self.inserted_money.get(coin, 0) + 1
  
  def addNote(self, note: Note):
    self.inserted_money[note] = self.inserted_money.get(note, 0) + 1
  
  def cancelTransaction(self):
    self.current_state.cancelTransaction()
  
  def getTotalPayment(self):
    return sum(k.value * v for k, v in self.inserted_money.items())

  def calculateChange(self, amount: float) -> dict:
    change_map = {}
    denominations = list(Note) + list(Coin)
    denominations.sort(key = lambda d: d.value, reverse = True)

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