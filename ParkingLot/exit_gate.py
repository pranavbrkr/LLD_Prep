from enums import PaymentMethod
from parking_lot import ParkingLot
from payment_processor import PaymentProcessor
from receipt import Receipt
from ticket_manager import TicketManager


class ExitGate:
  def __init__(self, lot: ParkingLot, ticket_manager: TicketManager, payment_processor: PaymentProcessor):
    self._lot = lot
    self._ticket_manager = ticket_manager
    self._payment_processor = payment_processor
  
  def processVehicleExit(self, ticket_id: str, method: PaymentMethod):
    ticket = self._ticket_manager.getTicketById(ticket_id)
    if not ticket:
      raise ValueError("Invalid or expired ticket ID")

    receipt: Receipt = self._payment_processor.pay(ticket, method)
    self._lot.vacateSpot(ticket)
    self._ticket_manager.removeTicket(ticket_id)

    print(f"Payment of amount ${receipt.getAmount():.2f} successful.")
    return receipt