from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base, TimestampMixin
from .enums import TradeType
if TYPE_CHECKING:
    from .portfolio import Portfolio  # noqa: F401
    from .execution import Execution  # noqa: F401


class Trade(Base, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), index=True)
    name = Column(String(200), index=True)
    type = Column(Enum(TradeType))
    initial_position = Column(Integer)
    initial_risk = Column(Float, nullable=True)
    current_position = Column(Integer)
    current_risk = Column(Float, nullable=True)
    profit_lost = Column(Float, nullable=True)
    started_at = Column(DateTime)
    closed_at = Column(DateTime, nullable=True)
    risk_ratio = Column(Float, nullable=True)
    commissions = Column(Float, default=0.0)
    portfolio_balance = Column(Float)

    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    portfolio = relationship("Portfolio", back_populates="trades")

    executions = relationship("Execution", back_populates="trade")
