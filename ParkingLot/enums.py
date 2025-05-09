from enum import Enum

class VehicleType(Enum):
  MOTORBIKE = "Motorbike"
  CAR = "Car"
  TRUCK = "Truck"

class PaymentMethod(Enum):
  CASH = "Cash"
  CARD = "Card"