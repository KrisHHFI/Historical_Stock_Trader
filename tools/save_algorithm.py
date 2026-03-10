import re
from pathlib import Path

ALGORITHMS_DIR = Path(__file__).parent.parent / "utils" / "trading_algorithms"


def save_algorithm(strategy_name: str, code: str) -> Path:
    safe_name = re.sub(r"[^a-z0-9_]", "", strategy_name.lower().replace(" ", "_"))
    filename = f"run_mock_{safe_name}_backtest.py"
    output_path = ALGORITHMS_DIR / filename
    output_path.write_text(code + "\n", encoding="utf-8")
    return output_path
