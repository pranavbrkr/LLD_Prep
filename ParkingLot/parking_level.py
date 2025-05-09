from collections import defaultdict
from typing import List
from enums import VehicleType
from parking_spot import ParkingSpot

class ParkingLevel:
  def __init__(self, level_number):
    self._level_number: int = level_number
    self._spots: List[ParkingSpot] = []

  def addSpot(self, spot: ParkingSpot):
    self._spots.append(spot)
  
  def getAvailableSpot(self, vehicle_type: VehicleType):
    for spot in self._spots:
      if spot.getSpotType() == vehicle_type and not spot.isOccupied():
        return spot
    return None

  def getLevelNumber(self):
    return self._level_number
  
  def getAvailableCount(self):
    count_map = defaultdict(int)
    for spot in self._spots:
      if not spot.isOccupied():
        count_map[spot.getSpotType()] += 1
    return count_map