from ticket import Ticket
from parking_lot import ParkingLot
from ticket_manager import TicketManager
from vehicle import Vehicle

class EntryGate:
  def __init__(self, lot: ParkingLot, ticket_manager: TicketManager):
    self._lot = lot
    self._ticket_manager = ticket_manager
  
  def processVehicleEntry(self, vehicle: Vehicle) -> Ticket:
    spot = self._lot.assignSpot(vehicle)
    if not spot:
      print(f"No spot available for vehicle type: {vehicle.getVehicleType()}")
      return None
    ticket = self._ticket_manager.generateTicket(vehicle, spot)
    print(f"Ticket ID {ticket.getTicketId()} issued for {vehicle.getLicensePlate()}")
    return ticket