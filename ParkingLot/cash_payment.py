from rate_card import RateCard
from receipt import Receipt
from payment_strategy import PaymentStrategy
from datetime import datetime

class CashPayment(PaymentStrategy):
  def pay(self, ticket):
    duration = (datetime.now() - ticket.getEntryTimestamp()).total_seconds() / 3600
    rate = RateCard.getRate(ticket.getVehicleType())
    amount = round(duration * rate, 2)
    print(f"Receipt generated for cash payment of ${amount}")
    return Receipt(amount, datetime.now())