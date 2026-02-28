"""
Aggregate collected per-csv backtest performance dictionaries into
a single combined performance summary.

Function: `aggregate_performances(collected_performances, tickers)`
- `collected_performances`: list of dicts produced by backtests
- `tickers`: list of ticker symbols corresponding to the performances

Returns a dict matching the structure expected by `build_performance_rows`.
"""
from typing import List, Dict


def aggregate_performances(collected_performances: List[Dict], tickers: List[str]) -> Dict:
    combined_initial = sum(p.get("initial_capital", 0.0) for p in collected_performances)
    combined_final = sum(p.get("final_capital", 0.0) for p in collected_performances)
    combined_net_pnl = sum(p.get("net_pnl", 0.0) for p in collected_performances)
    combined_fees = sum(p.get("total_fees_paid", 0.0) for p in collected_performances)
    combined_trade_count = sum(p.get("trade_count", 0) for p in collected_performances)
    combined_wins = sum(p.get("winning_trades", 0) for p in collected_performances)
    combined_losses = sum(p.get("losing_trades", 0) for p in collected_performances)

    combined_return_pct = (combined_net_pnl / combined_initial * 100) if combined_initial else 0.0
    combined_win_rate = (combined_wins / combined_trade_count * 100) if combined_trade_count else 0.0
    combined_avg_trade_return = (
        sum(p.get("avg_trade_return_pct", 0.0) * p.get("trade_count", 0) for p in collected_performances) / combined_trade_count
        if combined_trade_count else 0.0
    )

    performance = {
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
