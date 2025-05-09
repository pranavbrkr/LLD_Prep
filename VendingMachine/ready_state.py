from vending_machine_state import VendingMachineState

class ReadyState(VendingMachineState):
  def __init__(self, vending_machine):
    self.vending_machine = vending_machine
  
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