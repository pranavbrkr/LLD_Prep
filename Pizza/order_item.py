from abc import ABC, abstractmethod
from decimal import Decimal

class OrderItem(ABC):
  @abstractmethod
  def getPrice(self) -> Decimal:
    pass