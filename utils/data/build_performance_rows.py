"""Create display rows for a performance summary.

This module formats numeric values (currency, percentages, counts)
into a list of (label, string) tuples suitable for printing.
"""
from typing import Any, Dict, List, Tuple


def build_performance_rows(performance: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Return formatted performance rows.

    Args:
        performance: Dictionary containing performance metrics.
    """
    strategy = str(performance.get("strategy", ""))
    initial_capital = float(performance.get("initial_capital", 0.0))
    final_capital = float(performance.get("final_capital", 0.0))
    net_pnl = float(performance.get("net_pnl", 0.0))
    total_fees = float(performance.get("total_fees_paid", 0.0))
    return_pct = float(performance.get("return_pct", 0.0))
    trade_count = int(performance.get("trade_count", 0))
    winning_trades = int(performance.get("winning_trades", 0))
    losing_trades = int(performance.get("losing_trades", 0))
    win_rate_pct = float(performance.get("win_rate_pct", 0.0))
    avg_trade_return_pct = float(performance.get("avg_trade_return_pct", 0.0))

    return [
        ("Strategy", strategy),
        ("Initial capital", f"${initial_capital:,.2f}"),
        ("Final capital", f"${final_capital:,.2f}"),
        ("Net P&L", f"${net_pnl:,.2f}"),
        ("Total fees", f"${total_fees:,.2f}"),
        ("Return %", f"{return_pct:.2f}%"),
        ("Trades", str(trade_count)),
        ("Winning trades", str(winning_trades)),
        ("Losing trades", str(losing_trades)),
        ("Win rate", f"{win_rate_pct:.2f}%"),
        ("Average trade return", f"{avg_trade_return_pct:.2f}%"),
    ]
