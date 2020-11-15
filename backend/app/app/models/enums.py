from enum import Enum

class TradeType(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    CASH_IN = "CASH_IN"
    CASH_OUT = "CASH_OUT"

class ExecutionType(str, Enum):
    INITIAL = "INITIAL"
    ADD = "ADD"
    EXIT = "EXIT"

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