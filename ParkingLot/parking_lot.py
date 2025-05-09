from threading import Lock
from collections import defaultdict
from typing import List
from display_board import DisplayBoard
from parking_level import ParkingLevel
from ticket import Ticket
from vehicle import Vehicle


class ParkingLot:
  _instance = None
  _lock = Lock()

  def __init__(self):
    self._levels: List[ParkingLevel] = []
    self._display_board = DisplayBoard()
  
  @classmethod
  def getInstance(cls):
    with cls._lock:
      if cls._instance is None:
        cls._instance = cls()
    return cls._instance

  def addLevel(self, level: ParkingLevel):
    self._levels.append(level)
    self._updateDisplay()
  
  def assignSpot(self, vehicle: Vehicle):
    for level in self._levels:
      spot = level.getAvailableSpot(vehicle.getVehicleType())
      if spot:
        spot.assign(vehicle)
        self._display_board.update(vehicle.getVehicleType(), -1)
        return spot
    return None
  
  def vacateSpot(self, ticket: Ticket):
    spot = ticket.getAssignedSpot()
    spot.vacate()
    self._display_board.update(ticket.getVehicleType(), 1)
  
  def _updateDisplay(self):
    total_counts = defaultdict(int)
    for level in self._levels:
      level_counts = level.getAvailableCount()
      for v_type, count in level_counts.items():
        total_counts[v_type] += count
    self._display_board.setAvailability(total_counts)
  
  def getAvailability(self):
    self._display_board.show()