from enum import Enum

class TradeType(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    CASH_IN = "CASH_IN"
    CASH_OUT = "CASH_OUT"

class AdjustmentType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    INTERNAL_TRANSFER = "INTERNAL_TRANSFER"
    BROKER_INTEREST_PAID = "BROKER_INTEREST_PAID"
    ACCOUNT_TRANSFER = "ACCOUNT_TRANSFER"
    OTHER_FEES = "OTHER_FEES"
    INTEREST_YOU_PAID = "INTEREST_YOU_PAID"

class TradeStatus(str, Enum):
    OPEN = "OPEN"
    WIN = "WIN"
    LOSS = "LOSS"
    BE = "BE"

class ExecutionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class Currency(str, Enum):
    USD = "USD"
    CAD = "CAD"
    CNY = "CNY"
    EUR = "EUR"
    JPY = "JPY"

class ImpactType(str, Enum):
    POSITIVE = "POSITIVE"
    NEGTIVE = "NEGTIVE"
    NEUTRAL = "NEUTRAL"