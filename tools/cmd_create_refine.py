import re
import subprocess
import sys
from pathlib import Path

ML_OPTIMIZER_PATH = Path(__file__).parent.parent / "machine_learning" / "ml_optimizer.py"
ML_CONSTANTS_PATH = Path(__file__).parent.parent / "machine_learning" / "ml_constants.py"
ALGORITHMS_DIR = Path(__file__).parent.parent / "utils" / "trading_algorithms"
CONSTANTS_PATH = Path(__file__).parent.parent / "constants.py"


def _get_active_algo_name() -> str:
    content = CONSTANTS_PATH.read_text(encoding="utf-8")
    match = re.search(r"^active_algorithm\s*=\s*(\w+)", content, re.MULTILINE)
    return match.group(1) if match else ""


def _is_registered(algo_name: str) -> bool:
    content = ML_CONSTANTS_PATH.read_text(encoding="utf-8")
    return f'"{algo_name}"' in content


def _get_algo_source(algo_name: str) -> str:
    algo_file = ALGORITHMS_DIR / f"{algo_name}.py"
    if algo_file.exists():
        return algo_file.read_text(encoding="utf-8")
    return ""


def cmd_create_refine() -> None:
    algo_name = _get_active_algo_name()

    if algo_name and not _is_registered(algo_name):
        print(f"No ML param builder found for '{algo_name}'. Generating one...")
        sys.path.insert(0, str(Path(__file__).parent))
        from get_client import get_client
        from generate_ml_params_code import generate_ml_params_code
        from save_ml_params import save_ml_params

        strategy_name = re.sub(r"^run_mock_", "", algo_name)
        strategy_name = re.sub(r"_backtest$", "", strategy_name)

        algo_source = _get_algo_source(algo_name)
        client = get_client()
        params_code = generate_ml_params_code(client, strategy_name, algo_source)
        save_ml_params(strategy_name, params_code)
        print(f"ML param builder registered for '{algo_name}'.")

    subprocess.run(["python", str(ML_OPTIMIZER_PATH)], check=True)
