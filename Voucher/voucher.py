from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from threading import Lock
from typing import List


# Rule Strategy
class Rule(ABC):
  @abstractmethod
  def isSatisfied(self, user, cart):
    ...
  
class AgeRule(Rule):
  def __init__(self, min_age: int):
    self._min_age = min_age
  
  def isSatisfied(self, user, cart):
    return user.age >= self._min_age

class CartValueRule(Rule):
  def __init__(self, min_cart_value: Decimal):
    self._min_cart_value = min_cart_value
  
  def isSatisfied(self, user, cart):
    return cart.total >= self._min_cart_value


class DiscountStrategy(ABC):
  @abstractmethod
  def compute(self, cart):
    ...
  
class PercentageDiscount(DiscountStrategy):
  def __init__(self, percent):
    self._percent = percent
  
  def compute(self, cart):
    return cart.total * (1 - self._percent/100)
  
class FixedDiscount(DiscountStrategy):
  def __init__(self, fixed_amount):
    self._fixed_amount = fixed_amount
  
  def compute(self, cart):
    return self._fixed_amount


class CouponStatus(Enum):
  ACTIVE = auto()
  INACTIVE = auto()


class Coupon:
  _lock = Lock()

  def __init__(
    self, code, rules: List[Rule],
    overall_limit, per_user_limit, expiry, discount_strategy, status: CouponStatus = CouponStatus.ACTIVE
  ):
    self.code = code
    self.rules = rules
    self.overall_limit = overall_limit
    self.per_user_limit = per_user_limit
    self.expiry = expiry
    self.discount_strategy = discount_strategy
    self.status = status
    self.total_redemptions = 0
  
  def isEligible(self, user, cart, usage_repo):
    if self.status != CouponStatus.ACTIVE and self.expiry < datetime.now():
      return False

    if any(not rule.isSatisfied(user, cart) for rule in self.rules):
      return False
    
    with Coupon._lock:
      if self.total_redemptions >= self.overall_limit:
        return False
      if usage_repo.userCouponCount(user.id, self.code) >= self.per_user_limit:
        return False
    
    return True
  
  def redeem(self, user, usage_repo):
    with Coupon._lock:
      self.total_redemptions += 1
      usage_repo.incrementUserCoupon(user.id, self.code)

class VoucherStatus(Enum):
  UNUSED = auto()
  USED = auto()
  EXPIRED = auto()

class Voucher(ABC):
  def __init__(self, code, expiry: datetime):
    self.code = code
    self.expiry = expiry
    self.status = VoucherStatus.UNUSED
  
  @abstractmethod
  def canRedeem(self, user):
    ...
  
  def redeem(self):
    if self.isExpired():
      self.status = VoucherStatus.EXPIRED
    else:
      self.status = VoucherStatus.USED

  def isExpired(self):
    return datetime.now() > self.expiry

class UnassignedVoucher(Voucher):
  def canRedeem(self, user):
    return self.status == VoucherStatus.UNUSED and not self.isExpired()
  
class PreassignedVoucher(Voucher):
  def __init__(self, code, expiry, user_id):
    super().__init__(code, expiry)
    self.user_id = user_id

  def canRedeem(self, user):
    return (
      self.status == VoucherStatus.UNUSED and self.user_id == user.id and not self.isExpired()
    )