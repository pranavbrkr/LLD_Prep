from parking_spot import ParkingSpot
from ticket import Ticket
from vehicle import Vehicle

class TicketManager:
  def __init__(self):
    self._active_tickets = {}

  def generateTicket(self, vehicle: Vehicle, spot: ParkingSpot) -> Ticket:
    ticket = Ticket(vehicle.getLicensePlate(), vehicle.getVehicleType, spot)
    self._active_tickets[ticket.getTicketId()] = ticket
    return ticket

  def getTicketById(self, ticket_id: str):
    return self._active_tickets.get(ticket_id)

  def removeTicket(self, ticket_id: str):
    if ticket_id in self._active_tickets:
      del self._active_tickets[ticket_id]