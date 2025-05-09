from enums import VehicleType

class RateCard:
  _rates = {
    VehicleType.MOTORBIKE.value: 10.0,
    VehicleType.CAR.value: 15.0,
    VehicleType.TRUCK.value: 20.0,
  }

  @staticmethod
  def getRate(vehicle_type: VehicleType):
    return RateCard._rates.get(vehicle_type, 0.0)