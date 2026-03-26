from typing import Any, Callable
from pathlib import Path

from utils.data.build_file_metadata_rows import build_file_metadata_rows
from utils.data.build_stock_metadata_rows import build_stock_metadata_rows
from utils.data.parse_stock_filename_metadata import parse_stock_filename_metadata


def run_all_backtests(
    data_files: list[Path],
    active_algorithm: Callable,
    capital: int,
    transaction_fee_bps: float,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Run the active algorithm against every CSV file and collect results.

    Returns:
        performance_by_csv:   mapping of csv_path → performance dict
        collected_performances: list of performance dicts in file order
        tickers:              list of ticker symbols in file order
    """
    performance_by_csv: dict[str, dict[str, Any]] = {}
    collected_performances: list[dict[str, Any]] = []
    tickers: list[str] = []

    for stock_data_path in data_files:
        csv_path = str(stock_data_path)
        metadata = parse_stock_filename_metadata(csv_path)
        tickers.append(metadata["ticker"])

        performance = active_algorithm(
            csv_path=csv_path,
            initial_capital=capital,
            transaction_fee_bps=transaction_fee_bps,
        )
        performance_by_csv[csv_path] = performance
        collected_performances.append(performance)

    return performance_by_csv, collected_performances, tickers
