import time
from entry_gate import EntryGate
from enums import PaymentMethod, VehicleType
from exit_gate import ExitGate
from parking_level import ParkingLevel
from parking_lot import ParkingLot
from parking_spot import ParkingSpot
from payment_processor import PaymentProcessor
from ticket_manager import TicketManager
from vehicle import Vehicle

if __name__ == "__main__":
  lot = ParkingLot()
  ticket_manager = TicketManager()
  payment_processor = PaymentProcessor()

  level_0 = ParkingLevel(level_number=0)
  level_0.addSpot(ParkingSpot("0-A1", VehicleType.CAR))
  level_0.addSpot(ParkingSpot("0-A2", VehicleType.CAR))
  level_0.addSpot(ParkingSpot("0-B1", VehicleType.MOTORBIKE))
  level_0.addSpot(ParkingSpot("0-C1", VehicleType.TRUCK))

  lot.addLevel(level_0)

  print("\n--- Before Entry ---")
  lot.getAvailability()

  entry_gate = EntryGate(lot, ticket_manager)
  car = Vehicle("PABBI12", VehicleType.CAR)
  ticket = entry_gate.processVehicleEntry(car)

  time.sleep(2)

  print("\n--- After Entry ---")
  lot.getAvailability()

  exit_gate = ExitGate(lot, ticket_manager, payment_processor)
  receipt = exit_gate.processVehicleExit(ticket.getTicketId(), PaymentMethod.CARD)

  print("\n--- After Exit ---")
  lot.getAvailability()

  print(f"\n--- Receipt ---")
  print(f"Exit Time: {receipt.getExitTime()}")
  print(f"Amount Paid: ${receipt.getAmount():.2f}")