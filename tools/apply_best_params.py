import json
import re
from pathlib import Path

ML_BEST_PARAMS_FILE = Path(__file__).parent.parent / "ml_best_params.json"
ALGORITHMS_DIR = Path(__file__).parent.parent / "utils" / "trading_algorithms"


def apply_best_params() -> None:
    if not ML_BEST_PARAMS_FILE.exists():
        print("No best params file found — skipping apply step.")
        return

    with open(ML_BEST_PARAMS_FILE) as f:
        data = json.load(f)

    algo_name: str = data["algorithm"]
    params: dict = data["params"]
    avg_capital: float = data["avg_final_capital"]

    algo_file = ALGORITHMS_DIR / f"{algo_name}.py"
    if not algo_file.exists():
        print(f"Algorithm file not found: {algo_file}")
        return

    content = algo_file.read_text(encoding="utf-8")

    for param_name, value in params.items():
        if isinstance(value, float):
            formatted = str(round(value, 4))
        else:
            formatted = str(value)

        # Match: param_name: int/float = <old_value>
        content = re.sub(
            rf"(\b{re.escape(param_name)}\s*:\s*(?:int|float)\s*=\s*)[^\s,\n)]+",
            rf"\g<1>{formatted}",
            content,
        )

    algo_file.write_text(content, encoding="utf-8")
    print(f"Applied best params to {algo_name} (avg end capital: ${avg_capital:.2f})")
    for k, v in params.items():
        print(f"  {k} = {round(v, 4) if isinstance(v, float) else v}")
