from typing import Any

import pandas as pd


def execute_buy_trade(
    cash: float,
    close_price: float,
    trade_time: pd.Timestamp,
    transaction_fee_bps: float = 0.0,
) -> dict[str, Any]:
    fee_rate = abs(transaction_fee_bps) / 10000
    cost_per_share = close_price * (1 + fee_rate)
    shares_to_buy = int(cash // cost_per_share)
    if shares_to_buy <= 0:
        return {
            "cash": cash,
            "shares": 0,
            "buy_price": None,
            "buy_time": None,
            "entry_fee_paid": 0.0,
            "executed": False,
        }

    gross_cost = shares_to_buy * close_price
    entry_fee_paid = gross_cost * fee_rate
    total_cost = gross_cost + entry_fee_paid

    return {
        "cash": cash - total_cost,
        "shares": shares_to_buy,
        "buy_price": float(close_price),
        "buy_time": trade_time,
        "entry_fee_paid": float(entry_fee_paid),
        "executed": True,
    }
