from typing import List
from app.models import Trade, Execution
from app.models.enums import TradeType, TradeStatus, ExecutionType
from datetime import datetime

def test_calculate_trade_details() -> None: 
    trade: Trade = create_test_trade()
    trade.calculate_trade_details()
    assert trade.total_shares == 400
    assert trade.open_shares == 300
    assert trade.started_at == datetime(2017, 11, 20, 23, 55, 59, 0)
    assert trade.closed_at == None
    assert trade.status == TradeStatus.OPEN
    assert trade.commissions == 0
    assert trade.entry_price == 410
    assert trade.exit_price == 460
    assert trade.net_profit == 5000

    # close the trade
    trade.executions.append(create_execution(ExecutionType.SELL, 300, 480, datetime(2017, 11, 29, 23, 55, 59, 0)))
    trade.calculate_trade_details()
    assert trade.total_shares == 400
    assert trade.open_shares == 0
    assert trade.started_at == datetime(2017, 11, 20, 23, 55, 59, 0)
    assert trade.closed_at == datetime(2017, 11, 29, 23, 55, 59, 0)
    assert trade.status == TradeStatus.WIN
    assert trade.commissions == 0
    assert trade.entry_price == 410
    assert trade.exit_price == 475
    assert trade.net_profit == 26000.0
    assert trade.rmultiple == 65/30

def create_test_trade() -> Trade:
    trade: Trade = Trade()
    trade.ticker = "TSLA"
    trade.type = TradeType.LONG
    trade.stop_price = 380
    executions: List[Execution] = []
    executions.append(create_execution(ExecutionType.BUY, 200, 400, datetime(2017, 11, 28, 23, 55, 59, 0)))
    executions.append(create_execution(ExecutionType.BUY, 200, 420, datetime(2017, 11, 20, 23, 55, 59, 0)))
    executions.append(create_execution(ExecutionType.SELL, 100, 460, datetime(2017, 11, 28, 23, 55, 59, 0)))
    trade.executions = executions
    print(str(trade))
    return trade
    
def create_execution(type: ExecutionType, shares: int, price: float, execution_time: datetime) -> Execution:
    execution: Execution = Execution()
    execution.shares = shares
    execution.type = type
    execution.price = price
    execution.executed_at = execution_time
    return execution