"""Utilities for aggregating multiple per-CSV backtest performance dicts.

The primary exported function is :func:`aggregate_performances` which
combines a list of per-file performance dictionaries into a single
summary dictionary compatible with ``build_performance_rows``.
"""
from typing import Any, Dict, List


def aggregate_performances(
    collected_performances: List[Dict[str, Any]], tickers: List[str]
) -> Dict[str, Any]:
    """Aggregate a list of performance dicts into a single summary.

    Args:
        collected_performances: List of per-csv performance dictionaries
            produced by the backtests.
        tickers: List of ticker symbols corresponding to the performances.

    Returns:
        A dictionary containing aggregated performance metrics.
    """
    combined_initial: float = sum(
        float(p.get("initial_capital", 0.0)) for p in collected_performances
    )
    combined_final: float = sum(
        float(p.get("final_capital", 0.0)) for p in collected_performances
    )
    combined_net_pnl: float = sum(float(p.get("net_pnl", 0.0)) for p in collected_performances)
    combined_fees: float = sum(float(p.get("total_fees_paid", 0.0)) for p in collected_performances)
    combined_trade_count: int = sum(int(p.get("trade_count", 0)) for p in collected_performances)
    combined_wins: int = sum(int(p.get("winning_trades", 0)) for p in collected_performances)
    combined_losses: int = sum(int(p.get("losing_trades", 0)) for p in collected_performances)

    combined_return_pct: float = (
        (combined_net_pnl / combined_initial * 100.0) if combined_initial else 0.0
    )
    combined_win_rate: float = (
        (combined_wins / combined_trade_count * 100.0) if combined_trade_count else 0.0
    )

    combined_avg_trade_return: float
    if combined_trade_count:
        total_weighted = sum(
            float(p.get("avg_trade_return_pct", 0.0)) * int(p.get("trade_count", 0))
            for p in collected_performances
        )
        combined_avg_trade_return = total_weighted / combined_trade_count
    else:
        combined_avg_trade_return = 0.0

    performance: Dict[str, Any] = {
        "strategy": f"Combined ({', '.join(tickers)})",
        "initial_capital": combined_initial,
        "final_capital": combined_final,
        "net_pnl": combined_net_pnl,
        "total_fees_paid": combined_fees,
        "return_pct": combined_return_pct,
        "trade_count": combined_trade_count,
        "winning_trades": combined_wins,
        "losing_trades": combined_losses,
        "win_rate_pct": combined_win_rate,
        "avg_trade_return_pct": combined_avg_trade_return,
    }

    return performance
