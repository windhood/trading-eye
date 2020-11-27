from typing import Optional

from pydantic import BaseModel
from app.models.enums import TradeType
from datetime import datetime

# Shared properties
class TradeBase(BaseModel):
    # ticker: str
    name: Optional[str] = None
    type: Optional[TradeType] = None
    initial_position: Optional[int] = None
    initial_risk: Optional[float] = None
    current_position: Optional[int] = None
    current_risk: Optional[float] = None
    profit_lost: Optional[float] = None
    started_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    risk_ratio: Optional[float] = None
    commissions: Optional[float] = 0.0
    portfolio_balance: Optional[float] = None

    #portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    #portfolio = relationship("Portfolio", back_populates="trades")

    #executions = relationship("Execution", back_populates="trade")


# Properties to receive on Trade creation
class TradeCreate(TradeBase):
    ticker: str
    type: TradeType
    initial_position: int
    initial_risk: float
    current_position: int
    current_risk: float
    started_at: datetime
    portfolio_balance: float
    portfolio_id: int

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
