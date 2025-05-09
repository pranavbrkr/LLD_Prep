from collections import defaultdict
from enums import VehicleType

class DisplayBoard:
  def __init__(self):
    self._available_spots = defaultdict(int)
  
  def update(self, vehicle_type: VehicleType, delta: int):
    self._available_spots[vehicle_type] += delta
  
  def show(self):
    print("Available Spots:")
    for v_type, count in self._available_spots.items():
      print(f"{v_type}: {count}")
  
  def setAvailability(self, spot_counts: dict):
    self._available_spots = defaultdict(int, spot_counts)