import pandas as pd
from typing import Dict


def build_time_to_position(plot_data: pd.DataFrame, time_column: str) -> Dict[pd.Timestamp, int]:
    return {timestamp: idx for idx, timestamp in enumerate(plot_data[time_column])}
