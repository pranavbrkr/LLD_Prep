from abc import ABC, abstractmethod
from ticket import Ticket

class PaymentStrategy(ABC):
  @abstractmethod
  def pay(self, ticket: Ticket):
    pass