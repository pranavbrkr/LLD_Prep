from vending_machine_state import VendingMachineState

class ReturnChangeState(VendingMachineState):
  def __init__(self, vending_machine):
    self.vending_machine = vending_machine
  
  def selectProduct(self, product):
    print("Please collect the change first")
  
  def insertCoin(self, coin):
    print("Please collect the change first")
  
  def insertNote(self, note):
    print("Please collect the change first")
  
  def dispenseProduct(self):
    print("Product already dispensed. Please collect the change")
  
  def returnChange(self):
    change = self.vending_machine.total_payment - self.vending_machine.selected_product.getPrice()
    if change > 0:
      print(f"Change returned: ${change:.2f}")
      self.vending_machine.resetPayment()
    else:
      print("No change to return")
    self.vending_machine.resetSelectedProduct()
    self.vending_machine.setState(self.vending_machine.idle_state)