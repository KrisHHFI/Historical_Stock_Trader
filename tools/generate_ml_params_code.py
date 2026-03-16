from openai import OpenAI

ML_PARAMS_SYSTEM_PROMPT = """\
You are an expert Python quant developer. Output only a single raw Python function — \
no imports, no markdown, no code fences, no explanation.

The function must follow this exact signature:
    def _run_mock_<strategy_snake_case>_backtest_params(trial: optuna.Trial) -> dict[str, int | float]:

Rules:
1. Use only these Optuna call types: trial.suggest_int, trial.suggest_float.
2. Cover every tunable parameter in the algorithm's function signature \
   (exclude csv_path, initial_capital, transaction_fee_bps, entry_slippage_bps, \
   exit_slippage_bps, session_entry_start_minute, session_entry_end_minute).
3. Always include these five risk-control parameters with sensible ranges:
       stop_loss_pct:      trial.suggest_float("stop_loss_pct",     0.5, 3.0)
       take_profit_pct:    trial.suggest_float("take_profit_pct",   1.0, 5.0)
       trailing_stop_pct:  trial.suggest_float("trailing_stop_pct", 0.3, 2.0)
       max_hold_bars:      trial.suggest_int("max_hold_bars",       30, 300)
       cooldown_bars:      trial.suggest_int("cooldown_bars",        3,  30)
4. Choose realistic min/max ranges based on the algorithm's logic.
5. No print statements, no extra imports, no extra functions.
6. First character must be 'd' (start of 'def').
"""


def generate_ml_params_code(client: OpenAI, strategy_name: str, algo_code: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": ML_PARAMS_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Strategy name: {strategy_name}\n\n"
                    f"Algorithm source code:\n{algo_code}"
                ),
            },
        ],
        max_tokens=1024,
    )
    return (response.choices[0].message.content or "").strip()
