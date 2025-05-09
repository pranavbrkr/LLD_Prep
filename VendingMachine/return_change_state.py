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