from app.schemas.portfolio_adjustment import PortfolioAdjustment
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Enum, func
from sqlalchemy.orm import relationship

from datetime import datetime
from app.db.base_class import Base, TimestampMixin
from .enums import Currency, AdjustmentType

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .trade import Trade # noqa: F401


class Portfolio(Base, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=False)
    currency = Column(Enum(Currency))
    max_risk_per_share = Column(Float)
    max_risk_per_trade = Column(Float)
    max_capital_per_trade = Column(Float)
    initial_balance = Column(Float)
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    trades = relationship("Trade", back_populates="portfolio")
    adjustments = relationship("PortfolioAdjustment", back_populates="portfolio")

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="portfolios")

    def __repr__(self): 
        #return f'id={self.id}, title={self.title}, currency={self.currency}, '
        return f"""
            id={self.id}, title={self.title}, currency={self.currency},
            initial_balance={self.initial_balance}, owner_id={self.owner_id}
        """
     
    def adjust_balance(self) -> None: 
        if not self.adjustments:
            self.initial_balance = None
            return
        # https://www.johndcook.com/blog/2020/01/15/generator-expression/
        self.initial_balance = sum( self.value_of_adjustment(x) for x in self.adjustments )
    
    def value_of_adjustment(self, adjustment: PortfolioAdjustment) -> float:
        if adjustment.type == AdjustmentType.DEPOSIT \
            or  adjustment.type == AdjustmentType.BROKER_INTEREST_PAID:
            return adjustment.value
        return adjustment.value * (-1)

class PortfolioAdjustment(Base, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AdjustmentType), index=True)
    value = Column(Float)

    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    portfolio = relationship("Portfolio", back_populates="adjustments")

      