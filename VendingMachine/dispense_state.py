from vending_machine_state import VendingMachineState

class DispenseState(VendingMachineState):
  def __init__(self, vending_machine):
    self.vending_machine = vending_machine
  
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