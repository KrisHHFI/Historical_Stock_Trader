import pandas as pd


def get_time_column(df: pd.DataFrame) -> str:
    return "Datetime" if "Datetime" in df.columns else "Date"
