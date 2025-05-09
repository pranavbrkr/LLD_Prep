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
  def dispenseProduct(self):
    pass

  @abstractmethod
  def returnChange(self):
    pass