from enums import *


class Vehicle:
  def __init__(self, license_plate: str, vehicle_type: VehicleType):
    self._license_plate = license_plate
    self._vehicle_type = vehicle_type

  def getLicensePlate(self) -> str:
    return self._license_plate
  
  def getVehicleType(self) -> str:
    return self._vehicle_type.value
  