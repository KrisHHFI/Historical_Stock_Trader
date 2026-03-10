import sys
import re
from get_client import get_client
from get_strategy_name import get_strategy_name
from generate_algorithm_code import generate_algorithm_code
from save_algorithm import save_algorithm
from update_constants import update_constants

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        client = get_client()

        strategy_name = get_strategy_name(client)
        print(f"Strategy: {strategy_name}")

        print("Generating algorithm code...")
        code = generate_algorithm_code(client, strategy_name)

        output_path = save_algorithm(strategy_name, code)
        print(f"Saved to: {output_path}")

        update_constants(strategy_name, output_path)
        print(f"Updated constants.py: active_algorithm = run_mock_{re.sub(r'[^a-z0-9_]', '', strategy_name.lower().replace(' ', '_'))}_backtest")

