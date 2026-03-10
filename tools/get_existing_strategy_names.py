import re
from pathlib import Path

ALGORITHMS_DIR = Path(__file__).parent.parent / "utils" / "trading_algorithms"


def get_existing_strategy_names() -> list[str]:
    names = []
    for f in ALGORITHMS_DIR.glob("run_mock_*_backtest.py"):
        name = f.stem
        name = re.sub(r"^run_mock_", "", name)
        name = re.sub(r"_backtest$", "", name)
        names.append(name)
    return names
