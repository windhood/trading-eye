from typing import List, Optional

from pydantic import BaseModel
from app.models.enums import TradeType
from datetime import datetime
from .execution import Execution, ExecutionCreate

# Shared properties
class TradeBase(BaseModel):
    # ticker: str
    name: Optional[str] = None
    type: Optional[TradeType] = TradeType.LONG
    started_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    # risk_ratio: Optional[float] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    total_shares: Optional[int] = None
    open_shares: Optional[float] = None
    stop_price: Optional[float] = None
    target_price: Optional[float] = None
    net_profit: Optional[float] = None
    setup: Optional[str] = None
    rmultiple: Optional[float] = None
    commissions: Optional[float] = 0.0
    portfolio_balance: Optional[float] = None
    notes: Optional[str] = None

    #portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    #portfolio = relationship("Portfolio", back_populates="trades")

    #executions = relationship("Execution", back_populates="trade")


# Properties to receive on Trade creation
class TradeCreate(BaseModel):
    ticker: str
    portfolio_id: int
    executions: List[ExecutionCreate]

# Properties to receive on Trade update
class TradeUpdate(TradeBase):
    pass


# Properties shared by models stored in DB
class TradeInDBBase(TradeBase):
    id: int
    portfolio_id: int
    ticker: str

    class Config:
        orm_mode = True


# Properties to return to client
class Trade(TradeInDBBase):
    pass


# Properties properties stored in DB
class TradeInDB(TradeInDBBase):
    pass
