"""Build display rows for a file's metadata.

Returns a list of (label, value) tuples suitable for printing in tables.
"""
from typing import Any, Dict, List, Tuple
from datetime import datetime


def build_file_metadata_rows(metadata: Dict[str, Any], raw_data_folder: str) -> List[Tuple[str, str]]:
    """Return metadata rows for UI printing.

    Args:
        metadata: Parsed metadata for a CSV export.
        raw_data_folder: Path to the raw data folder (display only).
    """
    exported_at: datetime = metadata["exported_at"]
    return [
        ("File name", metadata["file_name"]),
        ("Export timestamp token", metadata["timestamp_token"]),
        ("Exported at", exported_at.strftime("%Y-%m-%d %H:%M:%S")),
        ("Export date", exported_at.strftime("%Y-%m-%d")),
        ("Export time", exported_at.strftime("%H:%M:%S")),
        ("File age", str(metadata["file_age"])),
        ("Stock data source", raw_data_folder),
    ]
