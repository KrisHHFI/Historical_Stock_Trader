"""Utilities for parsing stock CSV filenames.

The project expects filenames of the form
`<TICKER>_<INTERVAL>_<PERIOD>_<YYYYMMDD_HHMMSS>.csv`. This module provides a
single helper that extracts structured metadata from that name.
"""

from datetime import datetime
from pathlib import Path
import re
from typing import Any, Dict, Optional, Match


def parse_stock_filename_metadata(raw_data_folder: str | Path) -> Dict[str, Any]:
    """Parse metadata from a stock CSV filename.

    Args:
        raw_data_folder: Path or string pointing to the CSV file.

    Returns:
        A dict with keys like ``ticker``, ``interval``, ``period``,
        ``timestamp_token``, ``exported_at``, ``interval_quantity``,
        ``interval_unit``, ``is_max_history``, and ``file_age``.

    Raises:
        ValueError: If the filename doesn't match the expected pattern.
    """

    file_path = Path(raw_data_folder)
    file_name = file_path.name

    pattern = r"^(?P<ticker>[^_]+)_(?P<interval>[^_]+)_(?P<period>[^_]+)_(?P<timestamp>\d{8}_\d{6})\.csv$"
    match: Optional[Match[str]] = re.match(pattern, file_name)

    if not match:
        raise ValueError(
            "Invalid stock file name format. Expected: "
            "<ticker>_<interval>_<period>_<YYYYMMDD_HHMMSS>.csv"
        )

    ticker = match.group("ticker")
    interval = match.group("interval")
    period = match.group("period")
    timestamp_token = match.group("timestamp")
    exported_at = datetime.strptime(timestamp_token, "%Y%m%d_%H%M%S")

    interval_match: Optional[Match[str]] = re.match(r"^(\d+)([a-zA-Z]+)$", interval)
    interval_quantity: Optional[int] = (
        int(interval_match.group(1)) if interval_match else None
    )
    interval_unit: Optional[str] = interval_match.group(2) if interval_match else None

    is_max_history = period.lower() == "max"
    file_age = datetime.now() - exported_at

    return {
        "file_name": file_name,
        "ticker": ticker,
        "interval": interval,
        "period": period,
        "timestamp_token": timestamp_token,
        "exported_at": exported_at,
        "interval_quantity": interval_quantity,
        "interval_unit": interval_unit,
        "is_max_history": is_max_history,
        "file_age": file_age,
    }
