from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from order import Order

class Deal(ABC):
  @abstractmethod
  def calculateDiscount(self, order: 'Order') -> Decimal:
    pass