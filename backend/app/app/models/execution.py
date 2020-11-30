from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from app.db.base_class import Base, TimestampMixin
from .enums import ExecutionType

if TYPE_CHECKING:
    from .trade import Trade  # noqa: F401


class Execution(Base, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), index=True)
    price = Column(Float)
    shares = Column(Integer)
    commission = Column(Float, default=0.0)
    stop_price = Column(Float, nullable=True)
    target_price = Column(Float, nullable=True)
    type = Column(Enum(ExecutionType))
    executed_at = Column(DateTime)
    setup = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    trade_id = Column(Integer, ForeignKey("trade.id"))
    trade = relationship("Trade", back_populates="executions")
