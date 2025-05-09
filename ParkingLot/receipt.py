from datetime import datetime

class Receipt:
  def __init__(self, amount: float, exit_time: datetime):
    self._amount = amount
    self._exit_time = exit_time
  
  def getAmount(self):
    return self._amount
  
  def getExitTime(self):
    return self._exit_time