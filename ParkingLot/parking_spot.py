from enums import VehicleType
from vehicle import Vehicle


class ParkingSpot:
  def __init__(self, spot_id: str, spot_type: VehicleType):
    self._spot_id = spot_id
    self._spot_type = spot_type.value
    self._occupied = False
    self._vehicle = None

  def assign(self, vehicle: Vehicle):
    self._occupied = True
    self._vehicle = vehicle
  
  def vacate(self):
    self._occupied = False
    self._vehicle = None
  
  def isOccupied(self):
    return self._occupied
  
  def getVehicle(self):
    return self._vehicle
  
  def getSpotType(self):
    return self._spot_type
  
  def getSpotId(self):
    return self._spot_id