from typing import Any, Dict, List

from rich import box
from rich.console import Console
from rich.table import Table


def print_trades_table(trades: List[Dict[str, Any]]) -> None:
    console = Console()

    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.SQUARE,
        show_lines=True,
    )
    table.add_column("#", justify="right")
    table.add_column("Entry Time")
    table.add_column("Exit Time")
    table.add_column("Entry")
    table.add_column("Exit")
    table.add_column("Shares", justify="right")
    table.add_column("P&L", justify="right")
    table.add_column("Return %", justify="right")

    if not trades:
        table.add_row("-", "No trades", "-", "-", "-", "-", "-", "-")
    else:
        for trade in trades:
            entry_time = trade["entry_time"]
            exit_time = trade["exit_time"]

            formatted_entry_time = (
                entry_time.strftime("%Y-%m-%d %H:%M")
                if hasattr(entry_time, "strftime")
                else str(entry_time)
            )
            formatted_exit_time = (
                exit_time.strftime("%Y-%m-%d %H:%M")
                if hasattr(exit_time, "strftime")
                else str(exit_time)
            )

            entry_price = f"{trade['entry_price']:.2f}"
            exit_price = f"{trade['exit_price']:.2f}"
            shares = str(trade["shares"])
            pnl = f"${trade['pnl']:.2f}"
            return_pct = f"{trade['return_pct']:.2f}%"

            table.add_row(
                str(trade["trade"]),
                formatted_entry_time,
                formatted_exit_time,
                entry_price,
                exit_price,
                shares,
                pnl,
                return_pct,
            )

    console.print(table)
