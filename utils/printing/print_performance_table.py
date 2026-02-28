from rich.console import Console

from utils.printing.create_metadata_table import create_metadata_table


def print_performance_table(rows: list[tuple[str, str]]) -> None:
    console = Console()
    console.print(create_metadata_table(rows))
