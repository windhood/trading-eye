from typing import Optional

from pydantic import BaseModel


# Shared properties
class PortfolioBase(BaseModel):
    title: Optional[str] 
    description: Optional[str] = None
    currency: Optional[str] = "USD"
    max_risk_per_share: Optional[int] = None
    max_risk_per_trade: Optional[int] = None
    max_capital_per_trade: Optional[int] = None
    initial_balance: Optional[int]


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
