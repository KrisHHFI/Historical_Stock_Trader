import re
from pathlib import Path

ALGORITHMS_DIR = Path(__file__).parent.parent / "utils" / "trading_algorithms"
ML_CONSTANTS_PATH = Path(__file__).parent.parent / "machine_learning" / "ml_constants.py"
CONSTANTS_PATH = Path(__file__).parent.parent / "constants.py"


def discard_algorithm(strategy_name: str, prev_func_name: str) -> None:
    """Delete the generated algorithm and roll back constants.py and ml_constants.py."""
    safe_name = re.sub(r"[^a-z0-9_]", "", strategy_name.lower().replace(" ", "_"))
    func_name = f"run_mock_{safe_name}_backtest"
    param_func_name = f"_run_mock_{safe_name}_backtest_params"

    # 1. Delete the algorithm file
    algo_file = ALGORITHMS_DIR / f"{func_name}.py"
    if algo_file.exists():
        algo_file.unlink()
        print(f"  Deleted: {algo_file.name}")

    # 2. Remove the param builder function from ml_constants.py
    content = ML_CONSTANTS_PATH.read_text(encoding="utf-8")
    func_anchor = f"\n\ndef {param_func_name}("
    idx = content.find(func_anchor)
    if idx != -1:
        search_from = idx + 2
        next_def = content.find("\n\ndef ", search_from)
        registry_idx = content.find("\n\n# ──", search_from)
        candidates = [i for i in (next_def, registry_idx) if i != -1]
        end_idx = min(candidates) if candidates else len(content)
        content = content[:idx] + content[end_idx:]

    # Remove the registry entry line
    content = re.sub(
        rf'^\s*"{re.escape(func_name)}"\s*:.*,?\n',
        "",
        content,
        flags=re.MULTILINE,
    )
    ML_CONSTANTS_PATH.write_text(content, encoding="utf-8")
    print(f"  Removed from ml_constants.py: {func_name}")

    # 3. Restore constants.py to the previous algorithm
    if not prev_func_name:
        return

    module_name = f"utils.trading_algorithms.{prev_func_name}"
    import_line = f"from {module_name} import {prev_func_name}"

    constants_content = CONSTANTS_PATH.read_text(encoding="utf-8")
    lines = constants_content.splitlines()

    # Remove the discarded algorithm's import line
    discarded_import = re.compile(
        rf"^from utils\.trading_algorithms\.{re.escape(func_name)} import .*$"
    )
    lines = [line for line in lines if not discarded_import.match(line)]
    constants_content = "\n".join(lines) + "\n"

    # Add the previous algorithm's import back if it was removed
    if import_line not in constants_content:
        lines = constants_content.splitlines()
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("from utils.trading_algorithms"):
                insert_idx = i + 1
            elif "from pathlib import Path" in line and insert_idx == 0:
                insert_idx = i + 1
        lines.insert(insert_idx, import_line)
        constants_content = "\n".join(lines) + "\n"

    # Restore active_algorithm
    constants_content = re.sub(
        r"^active_algorithm\s*=.*$",
        f"active_algorithm = {prev_func_name}",
        constants_content,
        flags=re.MULTILINE,
    )
    CONSTANTS_PATH.write_text(constants_content, encoding="utf-8")
    print(f"  Restored constants.py → active_algorithm = {prev_func_name}")
