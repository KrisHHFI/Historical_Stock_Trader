"""Build display rows for a stock file's metadata.

Returns a list of (label, value) tuples suitable for printing in tables.
"""
from typing import Any, Dict, List, Tuple


def build_stock_metadata_rows(metadata: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Return stock metadata rows for UI printing.

    Args:
        metadata: Parsed metadata for a CSV export.
    """
    ticker = str(metadata.get("ticker", ""))
    interval = str(metadata.get("interval", ""))
    interval_quantity = str(metadata.get("interval_quantity", ""))
    interval_unit = str(metadata.get("interval_unit", ""))
    period = str(metadata.get("period", ""))

    return [
        ("Ticker", ticker),
        ("Interval", interval),
        ("Interval quantity", interval_quantity),
        ("Interval unit", interval_unit),
        ("Period", period),
    ]
