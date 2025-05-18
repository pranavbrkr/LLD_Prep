from datetime import datetime
from enum import Enum
from abc import ABC

class VehicleType(Enum):
  MOTORBIKE = "MOTORBIKE"
  CAR = "CAR"
  TRUCK = "TRUCK"

class Vehicle:
  def __init__(self, license_plate, vehicle_type):
    self.license_plate = license_plate
    self.vehicle_type = vehicle_type

class ParkingSpot:
  def __init__(self, spot_id, spot_type):
    self.spot_id = spot_id
    self.spot_type = spot_type
    self.occupied = False
  
  def isAvailable(self, vehicle_type):
    if (not self.occupied) and vehicle_type == self.spot_type:
      return self.spot_id
    else:
      return False
  
  def occupy(self):
    self.occupied = True
  
  def vacate(self):
    self.occupied = False

class ParkingLevel:
  def __init__(self, level_number, spots):
    self.level_number = level_number
    self.spots = spots
  
  def getAvailableSpot(self, vehicle_type):
    for spot in self.spots:
      if spot.isAvailable(vehicle_type):
        return spot
    return None

class ParkingLot:
  def __init__(self, levels):
    self.levels = levels

  def getAvailableSpot(self, vehicle_type):
    for level in self.levels:
      spot = level.getAvailableSpot(vehicle_type)
      if spot is not None:
        return level, spot
    
    return None

class Ticket:
  def __init__(self, vehicle, level, spot):
    self.vehicle = vehicle
    self.level = level
    self.spot = spot
    self.intime = datetime.now()
    self.outtime = None
  
  def closeTicket(self):
    self.outtime = datetime.now()

class TicketFactory:
  @staticmethod
  def createTicket(vehicle, level, spot):
    return Ticket(vehicle, level, spot)

class ParkingSpotManager:
  def __init__(self, parking_lot):
    self.parking_lot = parking_lot
  
  def findAvailableSpot(self, vehicle_type):
    return self.parking_lot.getAvailableSpot(vehicle_type)
  
  def occupySpot(self, spot):
    spot.occupy()
  
  def vacateSpot(self, spot):
    spot.vacate()

class TicketManager:
  def __init__(self):
    self.tickets = {}
  
  def issueTicket(self, vehicle, level, spot):
    ticket = TicketFactory.createTicket(vehicle, level, spot)
    self.tickets[vehicle.license_plate] = ticket
    return ticket

  def closeTicket(self, vehicle):
    ticket = self.tickets.pop(vehicle.license_plate, None)
    if ticket:
      ticket.closeTicket()
    return ticket

class PricingStrategy(ABC):
  def calculatePrice(self, ticket):
    pass

class FlatPricing(PricingStrategy):
  def calculatePrice(self, ticket):
    return 50

class HourlyRatePricing(PricingStrategy):
  def calculatePrice(self, ticket):
    duration = (ticket.intime - ticket.outtime).seconds // 3600 + 1
    return duration * 20

class PriceCalculator:
  def __init__(self, strategy):
    self.strategy = strategy
  
  def calculatePrice(self, ticket):
    return self.strategy.calculatePrice(ticket)

class PaymentStrategy(ABC):
  def pay(self, amount):
    pass
  
class CardPayment(PaymentStrategy):
  def pay(self, amount):
    print(f"Card payment of ${amount} completed")
  
class CashPayment(PaymentStrategy):
  def pay(self, amount):
    print(f"Cash payment of ${amount} completed")
  


class PaymentManager:
  def __init__(self, payment_strategy, pricing_strategy):
    self.payment_strategy = payment_strategy
    self.pricing_strategy = pricing_strategy

  def calculateAmount(self, ticket):
    calculator = PriceCalculator(self.pricing_strategy)
    return calculator.calculatePrice(ticket)

  def pay(self, amount):
    self.payment_strategy.pay(amount)
  
  def performPayment(self, ticket):
    amount = self.calculateAmount(ticket)
    self.pay(amount)

class ParkingLotService:
  def __init__(self, parking_spot_manager: ParkingSpotManager, ticket_manager: TicketManager):
    self.parking_spot_manager = parking_spot_manager
    self.ticket_manager = ticket_manager
  
  def parkVehicle(self, vehicle):
    result = self.parking_spot_manager.findAvailableSpot(vehicle.vehicle_type)
    if not result:
      print("No spot available")
    
    level, spot = result
    self.parking_spot_manager.occupySpot(spot)
    ticket = self.ticket_manager.issueTicket(vehicle, level, spot)

    print(f"Spot {spot.spot_id} assigned Level {level.level_number}")
  
  def unparkVehicle(self, vehicle):
    ticket = self.ticket_manager.closeTicket(vehicle)
    if not ticket:
      print("No active ticket found")
      return

    self.parking_spot_manager.vacateSpot(ticket.spot)
    payment_manager = PaymentManager(CardPayment(), HourlyRatePricing())
    payment_manager.performPayment(ticket)

if __name__ == "__main__":
  level0_spots = [ParkingSpot(f"0-{i}", VehicleType.TRUCK) for i in range(30)]
  level1_spots = [ParkingSpot(f"1-{i}", VehicleType.CAR) for i in range(30)]
  level0 = ParkingLevel(0, level0_spots)
  level1 = ParkingLevel(1, level1_spots)

  parking_lot = ParkingLot([level0, level1])
  parking_spot_manager = ParkingSpotManager(parking_lot)
  ticket_manager = TicketManager()
  parking_lot_service = ParkingLotService(parking_spot_manager, ticket_manager)
  vehicle1 = Vehicle("ABC123", VehicleType.CAR)
  vehicle2 = Vehicle("XZY789", VehicleType.TRUCK)

  parking_lot_service.parkVehicle(vehicle1)
  parking_lot_service.parkVehicle(vehicle2)

  import time
  time.sleep(5)

  parking_lot_service.unparkVehicle(vehicle2)