from typing import Optional

from pydantic import BaseModel
from app.models.enums import Currency

# Shared properties
class PortfolioBase(BaseModel):
    title: Optional[str] 
    description: Optional[str] = None
    currency: Optional[Currency] = Currency.USD
    max_risk_per_share: Optional[float] = None
    max_risk_per_trade: Optional[float] = None
    max_capital_per_trade: Optional[float] = None
    initial_balance: Optional[float]


# Properties to receive on item creation
class PortfolioCreate(PortfolioBase):
    title: str
    initial_balance: int


# Properties to receive on item update
class PortfolioUpdate(PortfolioBase):
    pass


# Properties shared by models stored in DB
class PortfolioInDBBase(PortfolioBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Portfolio(PortfolioInDBBase):
    pass


# Properties properties stored in DB
class PortfolioInDB(PortfolioInDBBase):
    pass
