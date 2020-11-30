from enum import Enum

class TradeType(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    CASH_IN = "CASH_IN"
    CASH_OUT = "CASH_OUT"

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