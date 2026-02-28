import matplotlib.pyplot as plt
import pandas as pd


def set_day_xticks(plot_data: pd.DataFrame, time_column: str) -> None:
    if len(plot_data) == 0:
        return
    trading_day = plot_data[time_column].dt.date
    day_start_positions = plot_data.groupby(trading_day, sort=False).head(1).index.tolist()
    day_labels = (
        plot_data.loc[day_start_positions, time_column].dt.strftime("%b %d").tolist()
    )
    plt.xticks(day_start_positions, day_labels, rotation=0, ha="center")
    plt.xlim(0, len(plot_data) - 1)
