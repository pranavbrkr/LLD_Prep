from datetime import datetime
import uuid
from enums import VehicleType
from parking_spot import ParkingSpot

class Ticket:
  def __init__(self, license_plate: str, vehicle_type: VehicleType, assigned_spot: ParkingSpot):
    self._ticket_id = str(uuid.uuid4())
    self._license_plate = license_plate
    self._vehicle_type = vehicle_type
    self._entry_timestamp = datetime.now()
    self._assigned_spot = assigned_spot

  def getTicketId(self):
    return self._ticket_id

  def getLicensePlate(self):
    return self._license_plate

  def getEntryTimestamp(self):
    return self._entry_timestamp

  def getVehicleType(self):
    return self._vehicle_type

  def getAssignedSpot(self):
    return self._assigned_spot