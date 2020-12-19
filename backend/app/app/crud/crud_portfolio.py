from app.schemas.portfolio_adjustment import PortfolioAdjustmentCreate
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.portfolio import Portfolio, PortfolioAdjustment
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.schemas.portfolio_adjustment import PortfolioAdjustmentCreate


class CRUDPortfolio(CRUDBase[Portfolio, PortfolioCreate, PortfolioUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: PortfolioCreate, owner_id: int
    ) -> Portfolio:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Portfolio]:
        return (
            db.query(self.model)
            .filter(Portfolio.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def add_adjustment(
        self, db: Session, *, portfolio: Portfolio, adjustment: PortfolioAdjustmentCreate
    ) -> Portfolio:
        entity = PortfolioAdjustment(**jsonable_encoder(adjustment), portfolio_id=portfolio.id)
        portfolio.adjustments.append(entity)
        portfolio.adjust_balance()
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        return portfolio

    def remove_adjustment(
        self, db: Session, *, portfolio: Portfolio, adjustment_id: int
    ) -> Portfolio:
        found_adjustments = [adjustment for adjustment in portfolio.adjustments if adjustment.id == adjustment_id]
        if not found_adjustments: 
            raise HTTPException(status_code=404, detail="adjustment not found")
        portfolio.adjustments.remove(found_adjustments[0])
        portfolio.adjust_balance()
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        return portfolio

portfolio = CRUDPortfolio(Portfolio)
