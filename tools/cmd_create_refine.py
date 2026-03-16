import subprocess
from pathlib import Path

ML_OPTIMIZER_PATH = Path(__file__).parent.parent / "machine_learning" / "ml_optimizer.py"


def cmd_create_refine() -> None:
    subprocess.run(["python", str(ML_OPTIMIZER_PATH)], check=True)
