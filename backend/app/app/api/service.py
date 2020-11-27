from app.models.portfolio import Portfolio
#from typing import Generator

from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from app import crud, models, schemas

from . import error_messages

def find_portfolio(
    db: Session,
    current_user: models.User, 
    portfolio_id: int 
) -> models.Portfolio:
    portfolio = crud.portfolio.get(db=db, id=portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail=error_messages.error_portfolio_not_found)
    if not crud.user.is_superuser(current_user) and (portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail=error_messages.error_not_enough_permission)
    return portfolio


