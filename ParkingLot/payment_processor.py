from payment_strategy import PaymentStrategy
from ticket import Ticket
from card_payment import CardPayment
from cash_payment import CashPayment
from enums import PaymentMethod

class PaymentProcessor:
  def __init__(self):
    self._strategies = {
      PaymentMethod.CASH: CashPayment(),
      PaymentMethod.CARD: CardPayment()
    }

  def pay(self, ticket: Ticket, method: PaymentMethod):
    strategy: PaymentStrategy = self._strategies.get(method)
    if strategy:
      return strategy.pay(ticket)
    else:
      raise ValueError(f"Unsupported payment method: {method}")