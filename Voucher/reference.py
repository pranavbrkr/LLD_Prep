from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from threading import Lock
from enum import Enum, auto
from decimal import Decimal


# ----------  Rule Strategy ----------
class Rule(ABC):
    @abstractmethod
    def is_satisfied(self, user, cart) -> bool: ...


class AgeRule(Rule):
    def __init__(self, min_age: int) -> None:
        self._min_age = min_age

    def is_satisfied(self, user, cart) -> bool:
        return user.age >= self._min_age


class CartValueRule(Rule):
    def __init__(self, min_cart_value: Decimal) -> None:
        self._min_value = min_cart_value

    def is_satisfied(self, user, cart) -> bool:
        return cart.total >= self._min_value


# ----------  Discount Strategy ----------
class DiscountStrategy(ABC):
    @abstractmethod
    def compute(self, cart) -> Decimal: ...


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def compute(self, cart) -> Decimal:
        return cart.total * Decimal(self.percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: Decimal):
        self.amount = amount

    def compute(self, cart) -> Decimal:
        return self.amount


# ----------  Coupon Aggregate ----------
class CouponStatus(Enum):
    ACTIVE = auto()
    INACTIVE = auto()


class Coupon:
    _lock = Lock()

    def __init__(
        self,
        code: str,
        rules: list[Rule],
        overall_limit: int,
        per_user_limit: int,
        expiry: datetime,
        discount_strategy: DiscountStrategy,
        status: CouponStatus = CouponStatus.ACTIVE,
    ) -> None:
        self.code = code
        self.rules = rules
        self.overall_limit = overall_limit
        self.per_user_limit = per_user_limit
        self.expiry = expiry
        self.discount_strategy = discount_strategy
        self.status = status
        self.total_redemptions = 0

    def is_eligible(self, user, cart, usage_repo) -> bool:
        if self.status != CouponStatus.ACTIVE or datetime.now() > self.expiry:
            return False

        if any(not rule.is_satisfied(user, cart) for rule in self.rules):
            return False

        with Coupon._lock:
            if self.total_redemptions >= self.overall_limit:
                return False
            if usage_repo.user_coupon_count(user.id, self.code) >= self.per_user_limit:
                return False

        return True

    def redeem(self, user, usage_repo) -> None:
        with Coupon._lock:
            self.total_redemptions += 1
            usage_repo.increment_user_coupon(user.id, self.code)


# ----------  Voucher Hierarchy ----------
class VoucherStatus(Enum):
    UNUSED = auto()
    USED = auto()
    EXPIRED = auto()


class Voucher(ABC):
    def __init__(self, code: str, expiry: datetime) -> None:
        self.code = code
        self.expiry = expiry
        self.status = VoucherStatus.UNUSED

    @abstractmethod
    def can_redeem(self, user) -> bool: ...

    def redeem(self) -> None:
        if self.is_expired():
            self.status = VoucherStatus.EXPIRED
        else:
            self.status = VoucherStatus.USED

    def is_expired(self) -> bool:
        return datetime.now() > self.expiry


class UnassignedVoucher(Voucher):
    def can_redeem(self, user) -> bool:
        return self.status == VoucherStatus.UNUSED and not self.is_expired()


class PreAssignedVoucher(Voucher):
    def __init__(self, code: str, expiry: datetime, user_id: str) -> None:
        super().__init__(code, expiry)
        self.user_id = user_id

    def can_redeem(self, user) -> bool:
        return (
            self.status == VoucherStatus.UNUSED
            and self.user_id == user.id
            and not self.is_expired()
        )


# ----------  Service Layer ----------
class RedemptionService:
    def __init__(self, coupon_repo, voucher_repo, usage_repo):
        self._coupon_repo = coupon_repo
        self._voucher_repo = voucher_repo
        self._usage_repo = usage_repo

    def apply_coupon(self, code, user, cart):
        coupon = self._coupon_repo.by_code(code)
        if coupon is None or not coupon.is_eligible(user, cart, self._usage_repo):
            return DiscountResult.invalid("Coupon not valid")

        coupon.redeem(user, self._usage_repo)
        self._coupon_repo.save(coupon)
        discount = coupon.discount_strategy.compute(cart)
        return DiscountResult.success(discount)

    def apply_voucher(self, code, user):
        voucher = self._voucher_repo.by_code(code)
        if voucher is None or not voucher.can_redeem(user):
            return DiscountResult.invalid("Voucher not valid")

        voucher.redeem()
        self._voucher_repo.save(voucher)
        return DiscountResult.success(Decimal("25.00"))  # example fixed discount


# ----------  DTO / Value objects ----------
class DiscountResult:
    def __init__(self, ok: bool, msg: str = "", value: Decimal = Decimal("0.0")):
        self.ok = ok
        self.msg = msg
        self.value = value

    @classmethod
    def success(cls, value): return cls(True, value=value)

    @classmethod
    def invalid(cls, msg): return cls(False, msg=msg)


# ----------  Supporting Mock Classes ----------
class User:
    def __init__(self, user_id, age):
        self.id = user_id
        self.age = age


class Cart:
    def __init__(self, total: Decimal):
        self.total = total


class UsageRepository:
    def __init__(self):
        self.user_coupon_usage = {}  # {user_id: {coupon_code: count}}

    def user_coupon_count(self, user_id, coupon_code):
        return self.user_coupon_usage.get(user_id, {}).get(coupon_code, 0)

    def increment_user_coupon(self, user_id, coupon_code):
        if user_id not in self.user_coupon_usage:
            self.user_coupon_usage[user_id] = {}
        if coupon_code not in self.user_coupon_usage[user_id]:
            self.user_coupon_usage[user_id][coupon_code] = 0
        self.user_coupon_usage[user_id][coupon_code] += 1


class CouponRepository:
    def __init__(self):
        self.coupons = {}

    def by_code(self, code):
        return self.coupons.get(code)

    def save(self, coupon):
        self.coupons[coupon.code] = coupon


class VoucherRepository:
    def __init__(self):
        self.vouchers = {}

    def by_code(self, code):
        return self.vouchers.get(code)

    def save(self, voucher):
        self.vouchers[voucher.code] = voucher


# ----------  Example Driver Code ----------
user = User("u123", 25)
cart = Cart(Decimal("120.00"))

coupon_repo = CouponRepository()
voucher_repo = VoucherRepository()
usage_repo = UsageRepository()

# Create a coupon: 10% off if age >= 18 and cart >= 100
rules = [AgeRule(18), CartValueRule(Decimal("100.00"))]
strategy = PercentageDiscount(10.0)
coupon = Coupon("SAVE10", rules, overall_limit=100, per_user_limit=2, expiry=datetime.now() + timedelta(days=1), discount_strategy=strategy)
coupon_repo.save(coupon)

# Create a voucher: unassigned and usable
voucher = UnassignedVoucher("WELCOME25", expiry=datetime.now() + timedelta(days=1))
voucher_repo.save(voucher)

service = RedemptionService(coupon_repo, voucher_repo, usage_repo)

# Apply coupon
result_coupon = service.apply_coupon("SAVE10", user, cart)

# Apply voucher
result_voucher = service.apply_voucher("WELCOME25", user)

result_coupon.ok, result_coupon.value, result_voucher.ok, result_voucher.value
