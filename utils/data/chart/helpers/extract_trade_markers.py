import pandas as pd
from typing import List, Optional, Tuple

from .build_time_to_position import build_time_to_position


def extract_trade_markers(
    plot_data: pd.DataFrame, time_column: str, trades: Optional[List[dict]]
) -> Tuple[List[int], List[float], List[int], List[float]]:
    buy_x: List[int] = []
    buy_y: List[float] = []
    sell_x: List[int] = []
    sell_y: List[float] = []

    if not trades:
        return buy_x, buy_y, sell_x, sell_y

    time_to_position = build_time_to_position(plot_data, time_column)

    for trade in trades:
        entry_time = pd.to_datetime(trade.get("entry_time"), errors="coerce")
        exit_time = pd.to_datetime(trade.get("exit_time"), errors="coerce")
        entry_price = trade.get("entry_price")
        exit_price = trade.get("exit_price")

        if pd.notna(entry_time) and entry_price is not None:
            entry_position = time_to_position.get(entry_time)
            if entry_position is not None:
                buy_x.append(entry_position)
                buy_y.append(float(entry_price))

        if pd.notna(exit_time) and exit_price is not None:
            exit_position = time_to_position.get(exit_time)
            if exit_position is not None:
                sell_x.append(exit_position)
                sell_y.append(float(exit_price))

    return buy_x, buy_y, sell_x, sell_y
