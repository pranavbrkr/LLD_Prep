from enum import Enum

class VehicleType(Enum):
  MOTORBIKE = 1
  CAR = 2
  TRUCK = 3

class PaymentMethod(Enum):
  CASH = "Cash"
  CARD = "Card"