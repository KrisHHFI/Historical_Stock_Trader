import matplotlib.pyplot as plt
from pathlib import Path
from typing import Any

from .helpers.load_and_prepare_data import load_and_prepare_data
from .helpers.extract_trade_markers import extract_trade_markers
from .helpers.plot_trade_markers import plot_trade_markers
from .helpers.set_day_xticks import set_day_xticks


def plot_compressed_trading_chart(
    csv_path: str,
    ticker: str,
    interval: str,
    trades: list[dict[str, Any]] | None = None,
) -> None:
    plot_data, time_column = load_and_prepare_data(csv_path)

    x_positions = range(len(plot_data))

    figure = plt.figure(figsize=(12, 5))
    if hasattr(figure.canvas, "header_visible"):
        figure.canvas.header_visible = False
    plt.plot(x_positions, plot_data["Close"], linewidth=1)

    buy_x, buy_y, sell_x, sell_y = extract_trade_markers(plot_data, time_column, trades)
    plot_trade_markers(buy_x, buy_y, sell_x, sell_y)

    plt.title(Path(csv_path).name)
    plt.xlabel("Trading Time (compressed)")
    plt.ylabel("Close Price")
    plt.grid(True, alpha=0.3)
    plt.margins(x=0)

    set_day_xticks(plot_data, time_column)

    plt.tight_layout()
    plt.show()
