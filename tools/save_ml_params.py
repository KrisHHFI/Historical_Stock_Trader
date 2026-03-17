import re
from pathlib import Path
from strip_markdown_fences import strip_markdown_fences

ML_CONSTANTS_PATH = Path(__file__).parent.parent / "machine_learning" / "ml_constants.py"


def save_ml_params(strategy_name: str, params_func_code: str) -> None:
    safe_name = re.sub(r"[^a-z0-9_]", "", strategy_name.lower().replace(" ", "_"))
    func_name = f"_run_mock_{safe_name}_backtest_params"
    registry_key = f"run_mock_{safe_name}_backtest"

    params_func_code = strip_markdown_fences(params_func_code)

    content = ML_CONSTANTS_PATH.read_text(encoding="utf-8")

    # Skip if already registered
    if registry_key in content:
        return

    # Insert the param builder function before the REGISTRY section
    registry_marker = "# ── REGISTRY"
    if registry_marker not in content:
        return

    func_block = f"\n\n{params_func_code}\n"
    content = content.replace(registry_marker, func_block + registry_marker)

    # Insert the new entry into ML_PARAM_BUILDERS before the closing }
    new_entry = f'    "{registry_key}":{" " * max(1, 50 - len(registry_key))}{func_name},'
    content = re.sub(
        r"(ML_PARAM_BUILDERS: dict\[.*?\] = \{.*?)(^\})",
        lambda m: m.group(1) + new_entry + "\n" + m.group(2),
        content,
        flags=re.DOTALL | re.MULTILINE,
    )

    ML_CONSTANTS_PATH.write_text(content, encoding="utf-8")
