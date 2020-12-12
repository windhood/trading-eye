from app.schemas.execution import ExecutionCreate
import logging
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps, service, error_messages

router = APIRouter()


@router.get("/", response_model=List[schemas.Trade])
def read_trades(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    portfolio_id: Optional[int] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tradess.
    """
    if crud.user.is_superuser(current_user):
        trades = crud.trade.get_multi(db, skip=skip, limit=limit)
    elif portfolio_id:
        portfolio = service.find_portfolio(db, current_user, portfolio_id)
        logging.debug(f"portfolio is: {portfolio}")
        trades = crud.trade.get_multi_by_portfolio(db, portfolio_id=portfolio_id,skip=skip, limit=limit)
    else:
        trades = crud.trade.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return trades


@router.post("/", response_model=schemas.Trade)
def create_trade(
    *,
    db: Session = Depends(deps.get_db),
    trade_in: schemas.NewTrade,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new trade.
    """
    if not trade_in.portfolio_id: #empty
        raise HTTPException(status_code=400, detail=error_messages.error_missing_parameter)
    portfolio = service.find_portfolio(db, current_user, trade_in.portfolio_id)
    logging.debug(f"portfolio is: {portfolio}")
    # trade = crud.trade.create_with_owner(db=db, obj_in=trade_in, owner_id=current_user.id)
    # trade = crud.trade.create_with_portfolio(db=db, obj_in=trade_in, portfolio_id= trade_in.portfolio_id)
    trade = crud.trade.create_with_executions(db=db, obj_in=trade_in, portfolio=portfolio)
    # TODO should create first execution too
    return trade


@router.put("/{id}", response_model=schemas.Trade)
def update_trade(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    trade_in: schemas.TradeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an trade.
    """
    trade = crud.trade.get(db=db, id=id)
    if not trade:
        raise HTTPException(status_code=404, detail=error_messages.error_trade_not_found)
    if not crud.user.is_superuser(current_user) and (trade.portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail=error_messages.error_not_enough_permission)
    trade = crud.trade.update(db=db, db_obj=trade, obj_in=trade_in)
    return trade


@router.get("/{id}", response_model=schemas.TradeDetail)
def read_trade(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get trade by ID.
    """
    trade = crud.trade.get(db=db, id=id)
    if not trade:
        raise HTTPException(status_code=404, detail=error_messages.error_trade_not_found)
    if not crud.user.is_superuser(current_user) and (trade.portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail=error_messages.error_not_enough_permission)
    return trade


@router.delete("/{id}", response_model=schemas.Trade)
def delete_trade(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an trade.
    """
    trade = crud.trade.get(db=db, id=id)
    if not trade:
        raise HTTPException(status_code=404, detail=error_messages.error_trade_not_found)
    if not crud.user.is_superuser(current_user) and (trade.portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail=error_messages.error_not_enough_permission)
    trade = crud.trade.remove(db=db, id=id)
    return trade

'''
Routes to handle executions
'''
@router.post("/{id}/executions", response_model=schemas.TradeDetail)
def add_executions(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    executions: List[ExecutionCreate],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a list of executions to a trade.
    """
    trade = crud.trade.get(db=db, id=id)
    if not trade:
        raise HTTPException(status_code=404, detail=error_messages.error_trade_not_found)
    if not crud.user.is_superuser(current_user) and (trade.portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail=error_messages.error_not_enough_permission)
    
    trade = crud.trade.add_executions(db=db, trade=trade, executions=executions)
    # TODO should create first execution too
    return trade

@router.put("/{trade_id}/executions/{id}", response_model=schemas.TradeDetail)
def update_execution(
    *,
    db: Session = Depends(deps.get_db),
    trade_id: int,
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a list of executions to a trade.
    """
    trade = crud.trade.get(db=db, id=id)
    if not trade:
        raise HTTPException(status_code=404, detail=error_messages.error_trade_not_found)
    if not crud.user.is_superuser(current_user) and (trade.portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail=error_messages.error_not_enough_permission)
    
    trade = crud.trade.add_executions(db=db, trade=trade, executions=executions)
    # TODO should create first execution too
    return trade