import re
from pathlib import Path

CONSTANTS_PATH = Path(__file__).parent.parent / "constants.py"


def update_constants(strategy_name: str, output_path: Path) -> None:
    if not output_path.exists():
        print(f"Skipping constants.py update — file not found: {output_path}")
        return
    safe_name = re.sub(r"[^a-z0-9_]", "", strategy_name.lower().replace(" ", "_"))
    func_name = f"run_mock_{safe_name}_backtest"
    module = f"utils.trading_algorithms.run_mock_{safe_name}_backtest"
    import_line = f"from {module} import {func_name}"

    content = CONSTANTS_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Find and remove the old active_algorithm import (the uncommented one)
    old_func_match = re.search(r"^active_algorithm\s*=\s*(\w+)", content, re.MULTILINE)
    if old_func_match:
        old_func_name = old_func_match.group(1)
        if old_func_name != func_name:
            lines = [
                line for line in lines
                if not re.match(rf"^from utils\.trading_algorithms\.\S+ import {re.escape(old_func_name)}\s*$", line)
            ]

    # Add new import if not already present
    content = "\n".join(lines) + "\n"
    if import_line not in content:
        lines = content.splitlines()
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("from utils.trading_algorithms"):
                insert_idx = i + 1
            elif "from pathlib import Path" in line and insert_idx == 0:
                insert_idx = i + 1
        lines.insert(insert_idx, import_line)
        content = "\n".join(lines) + "\n"

    # Update active_algorithm
    content = re.sub(
        r"^active_algorithm\s*=.*$",
        f"active_algorithm = {func_name}",
        content,
        flags=re.MULTILINE,
    )

    CONSTANTS_PATH.write_text(content, encoding="utf-8")
