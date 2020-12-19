from typing import Optional

from pydantic import BaseModel
from app.models.enums import AdjustmentType
from datetime import datetime

# Shared properties
class PortfolioAdjustmentBase(BaseModel):
    type: Optional[AdjustmentType] 
    value: Optional[float]
    created_at: Optional[datetime]

# Properties to receive on item creation
class PortfolioAdjustmentCreate(PortfolioAdjustmentBase):
    type: AdjustmentType
    value: float
    created_at: datetime


# Properties to receive on item update
class PortfolioAdjustmentUpdate(PortfolioAdjustmentBase):
    pass


# Properties shared by models stored in DB
class PortfolioAdjustmentInDBBase(PortfolioAdjustmentBase):
    id: int
    portfolio_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class PortfolioAdjustment(PortfolioAdjustmentInDBBase):
    pass


# Properties properties stored in DB
class PortfolioAdjustmentInDB(PortfolioAdjustmentInDBBase):
    pass
