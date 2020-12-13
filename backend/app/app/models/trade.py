from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Float, DateTime, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base, TimestampMixin
from .enums import TradeType, TradeStatus, ExecutionType
if TYPE_CHECKING:
    from .portfolio import Portfolio  # noqa: F401
    from .execution import Execution  # noqa: F401


class Trade(Base, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), index=True)
    name = Column(String(200), index=True)
    type = Column(Enum(TradeType))
    #initial_position = Column(Integer)
    #initial_risk = Column(Float, nullable=True)
    #current_position = Column(Integer)
    #current_risk = Column(Float, nullable=True)
    #profit_lost = Column(Float, nullable=True) 
    started_at = Column(DateTime)
    closed_at = Column(DateTime, nullable=True)
    #risk_ratio = Column(Float, nullable=True)    

    entry_price = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)
    total_shares = Column(Integer, nullable=True)
    open_shares = Column(Integer, nullable=True)
    stop_price = Column(Float, nullable=True)
    target_price = Column(Float, nullable=True)
    net_profit = Column(Float, nullable=True) 
    setup = Column(String, nullable=True)
    rmultiple = Column(Float, nullable=True)
    commissions = Column(Float, default=0.0)
    portfolio_balance = Column(Float)
    status = Column(Enum(TradeStatus))
    notes = Column(Text, nullable=True)

    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    portfolio = relationship("Portfolio", back_populates="trades")

    executions = relationship("Execution", back_populates="trade")
    
    def __repr__(self): 
        return f'tiker={self.ticker}, executions={self.executions}'
     
    def calculate_trade_details(self) -> None:         
        #customObjects.sort(key=lambda x: x.date, reverse=True)        
        self.executions.sort(key=lambda x: x.executed_at.timestamp())
        self.started_at = self.executions[0].executed_at        
        self.commissions = 0

        entry_shares : int = 0
        exit_shares = 0
        entry_total = 0
        exit_total = 0
        for execution in self.executions:
            if execution.commission:
                self.commissions += execution.commission
            if execution.type == ExecutionType.BUY:
                entry_shares +=execution.shares
                entry_total += execution.price * execution.shares
                
            elif execution.type == ExecutionType.SELL:
                exit_shares +=execution.shares
                exit_total += execution.price * execution.shares
        
        self.total_shares = entry_shares
        self.open_shares = entry_shares - exit_shares
        
        if entry_shares > 0:
            self.entry_price = entry_total/entry_shares
        if exit_shares > 0:
            self.exit_price = exit_total/exit_shares
            # realized net profit
            self.net_profit = exit_shares * (self.exit_price - self.entry_price) - self.commissions


        if self.open_shares == 0:
            self.closed_at = self.executions[-1].executed_at
            if self.net_profit > 10:
                self.status = TradeStatus.WIN
            elif self.net_profit < -10:
                self.status = TradeStatus.LOSS
            else:
                self.status = TradeStatus.BE
        else:
            self.closed_at = None
            self.status = TradeStatus.OPEN
        
        # calculate r-multile
        if self.open_shares == 0 and self.stop_price:
            self.rmultiple = (self.exit_price - self.entry_price)/(self.entry_price - self.stop_price)

        