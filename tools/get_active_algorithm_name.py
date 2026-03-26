import re
from pathlib import Path

CONSTANTS_PATH = Path(__file__).parent.parent / "constants.py"


def get_active_algorithm_name() -> str:
    """Return the current active_algorithm function name from constants.py."""
    content = CONSTANTS_PATH.read_text(encoding="utf-8")
    match = re.search(r"^active_algorithm\s*=\s*(\w+)", content, re.MULTILINE)
    return match.group(1) if match else ""
