from enum import Enum

class Coin(Enum):
  PENNY = 0.01
  NICKEL = 0.05
  DIME = 0.1
  QUARTER = 0.25

class Note(Enum):
  ONE = 1
  FIVE = 5
  TEN = 10
  TWENTY = 20