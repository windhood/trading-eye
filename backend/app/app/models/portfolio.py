from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from datetime import datetime
from app.db.base_class import Base, TimestampMixin


if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Portfolio(Base, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=False)
    currency = Column(String(20))
    max_risk_per_share = Column(Integer)
    max_risk_per_trade = Column(Integer)
    max_capital_per_trade = Column(Integer)
    initial_balance = Column(Integer)
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="portfolios")
    
