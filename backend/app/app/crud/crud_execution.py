from app.models.trade import Trade
from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.execution import Execution
from app.schemas.execution import ExecutionCreate, ExecutionUpdate


class CRUDExecution(CRUDBase[Execution, ExecutionCreate, ExecutionUpdate]):
    def create_with_trade(
        self, db: Session, *, obj_in: ExecutionCreate, trade_id: int
    ) -> Execution:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, trade_id=trade_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_trade(
        self, db: Session, *, trade_id: int, skip: int = 0, limit: int = 100
    ) -> List[Execution]:
        return (
            db.query(self.model)
            .filter(Execution.trade_id == trade_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    def update_entity(
        self, 
        db_obj: Execution,
        obj_in: Union[ExecutionUpdate, Dict[str, Any]]) -> Execution:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return db_obj

execution = CRUDExecution(Execution)
