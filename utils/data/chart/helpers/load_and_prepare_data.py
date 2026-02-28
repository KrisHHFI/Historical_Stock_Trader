import pandas as pd
from typing import Tuple

from .get_time_column import get_time_column


def load_and_prepare_data(csv_path: str) -> Tuple[pd.DataFrame, str]:
    price_data = pd.read_csv(csv_path)
    time_column = get_time_column(price_data)
    price_data[time_column] = pd.to_datetime(price_data[time_column], errors="coerce")
    plot_data = (
        price_data.dropna(subset=[time_column])
        .sort_values(time_column)
        .reset_index(drop=True)
    )
    return plot_data, time_column
