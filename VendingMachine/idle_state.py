from vending_machine_state import VendingMachineState

class IdleState(VendingMachineState):
  def __init__(self, vending_machine):
    self.vending_machine = vending_machine

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