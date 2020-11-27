from app.models.portfolio import Portfolio
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeUpdate


class CRUDTrade(CRUDBase[Trade, TradeCreate, TradeCreate]):
    def create_with_portfolio(
        self, db: Session, *, obj_in: TradeCreate, portfolio_id: int
    ) -> Trade:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, portfolio_id=portfolio_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_portfolio(
        self, db: Session, *, portfolio_id: int, skip: int = 0, limit: int = 100
    ) -> List[Trade]:
        return (
            db.query(self.model)
            .filter(Trade.portfolio_id == portfolio_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Trade]:
        return (
            db.query(self.model)
            .join(Trade.portfolio)
            .filter(Portfolio.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    

trade = CRUDTrade(Trade)
