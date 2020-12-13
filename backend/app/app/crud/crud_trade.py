from app.schemas.execution import ExecutionCreate
from app.models.portfolio import Portfolio
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeUpdate, NewTrade
from app.models.execution import Execution


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

    def create_with_executions(
        self, db: Session, *, obj_in: NewTrade, portfolio: Portfolio
    ) -> Trade:
        # obj_in_data = jsonable_encoder(obj_in)
        # db_obj = self.model(**obj_in_data)
        db_obj = self.build_model_from(obj_in, portfolio)
        db_obj.calculate_trade_details()
        #db_obj = self.setup_from_executions(db_obj)
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

    def add_executions(
        self, db: Session, *, trade: Trade, executions: List[ExecutionCreate]
    ) -> Trade:
        for ex in executions:
            entity = Execution(**jsonable_encoder(ex), ticker=trade.ticker)
            entity.executed_at = ex.executed_at
            trade.executions.append(entity)
        #execution_models: List[Execution] = [Execution(**jsonable_encoder(el), executed_at=el.executed_at, ticker=trade.ticker) for el in executions]
        #for ex in execution_models:
        #    print(f'object is {ex}, executed_at type is {type(ex.executed_at)}, isinstanceof: {isinstance(ex.executed_at, str)}')
        #trade.executions.extend(execution_models)
        print("\nafter merge")
        for ex in trade.executions:
            print(f'object is:{ex}, type is {type(ex)}, executed_at type is {type(ex.executed_at)}')
            
        trade.calculate_trade_details()
        db.add(trade)
        db.commit()
        db.refresh(trade)
        return trade

    def update_execution(
        self, db: Session, *, trade: Trade
    ) -> Trade:
        trade.calculate_trade_details()
        db.add(trade)
        db.commit()
        db.refresh(trade)
        return trade

    def build_model_from(self, obj_in: NewTrade, portfolio: Portfolio) -> Trade: 
        trade_model = self.model(ticker=obj_in.ticker, portfolio_id=obj_in.portfolio_id)
        trade_model.name = obj_in.ticker
        trade_model.type = obj_in.type
        trade_model.portfolio_balance = portfolio.initial_balance
        execution_models: List[Execution] = [Execution(**jsonable_encoder(el), ticker=obj_in.ticker) for el in obj_in.executions]
        trade_model.executions = execution_models
        return trade_model
    

trade = CRUDTrade(Trade)
