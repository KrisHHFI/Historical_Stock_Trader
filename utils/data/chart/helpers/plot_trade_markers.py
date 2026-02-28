import matplotlib.pyplot as plt
from typing import List


def plot_trade_markers(
    buy_x: List[int], buy_y: List[float], sell_x: List[int], sell_y: List[float]
) -> None:
    if buy_x:
        plt.scatter(buy_x, buy_y, marker="^", color="green", s=45, label="Buy", zorder=3)
    if sell_x:
        plt.scatter(sell_x, sell_y, marker="v", color="red", s=45, label="Sell", zorder=3)
    if buy_x or sell_x:
        plt.legend(loc="best")
