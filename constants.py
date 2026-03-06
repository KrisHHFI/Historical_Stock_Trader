from utils.trading_algorithms.run_mock_ema_crossover_backtest import run_mock_ema_crossover_backtest
#from utils.trading_algorithms.run_mock_vwap_ema_crossover_backtest import run_mock_vwap_ema_crossover_backtest

raw_data_folder: str = "/Users/kristopherpepper/Documents/jupyterProjects/historicalStockTrader2/raw_data"

# Trading
capital: int = 10000
transaction_fee_bps: float = 1.0
active_algorithm = run_mock_ema_crossover_backtest
