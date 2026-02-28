import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def plot_compressed_trading_chart(
    csv_path: str,
    ticker: str,
    interval: str,
    trades: list[dict] | None = None,
) -> None:
    price_data = pd.read_csv(csv_path)

    time_column = "Datetime" if "Datetime" in price_data.columns else "Date"
    price_data[time_column] = pd.to_datetime(price_data[time_column], errors="coerce")
    plot_data = (
        price_data.dropna(subset=[time_column])
        .sort_values(time_column)
        .reset_index(drop=True)
    )

    x_positions = range(len(plot_data))

    figure = plt.figure(figsize=(12, 5))
    if hasattr(figure.canvas, "header_visible"):
        figure.canvas.header_visible = False
    plt.plot(x_positions, plot_data["Close"], linewidth=1)

    if trades:
        time_to_position = {
            timestamp: idx for idx, timestamp in enumerate(plot_data[time_column])
        }

        buy_x: list[int] = []
        buy_y: list[float] = []
        sell_x: list[int] = []
        sell_y: list[float] = []

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

        if buy_x:
            plt.scatter(buy_x, buy_y, marker="^", color="green", s=45, label="Buy", zorder=3)
        if sell_x:
            plt.scatter(sell_x, sell_y, marker="v", color="red", s=45, label="Sell", zorder=3)
        if buy_x or sell_x:
            plt.legend(loc="best")

    plt.title(Path(csv_path).name)
    plt.xlabel("Trading Time (compressed)")
    plt.ylabel("Close Price")
    plt.grid(True, alpha=0.3)
    plt.margins(x=0)

    if len(plot_data) > 0:
        trading_day = plot_data[time_column].dt.date
        day_start_positions = (
            plot_data.groupby(trading_day, sort=False).head(1).index.tolist()
        )
        day_labels = (
            plot_data.loc[day_start_positions, time_column]
            .dt.strftime("%b %d")
            .tolist()
        )
        plt.xticks(day_start_positions, day_labels, rotation=0, ha="center")
        plt.xlim(0, len(plot_data) - 1)

    plt.tight_layout()
    plt.show()
