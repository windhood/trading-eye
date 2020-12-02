from typing import Optional

from pydantic import BaseModel
from app.models.enums import ExecutionType
from datetime import datetime
# Shared properties
class ExecutionBase(BaseModel):
    ticker: str
    price: Optional[float] = None
    shares: Optional[int] = None
    commission: Optional[float] = 7.00
    stop_price: Optional[float] = None
    target_price: Optional[float] = None
    type: ExecutionType
    executed_at: datetime = datetime.now
    setup: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


# Properties to receive on item creation
class ExecutionCreate(ExecutionBase):
    price: float
    shares: int    


# Properties to receive on item update
class ExecutionUpdate(ExecutionBase):
    pass


# Properties shared by models stored in DB
class ExecutionInDBBase(ExecutionBase):
    id: int
    trade_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Execution(ExecutionInDBBase):
    pass


# Properties properties stored in DB
class ExecutionInDB(ExecutionInDBBase):
    pass
