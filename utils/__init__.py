try:
	# primary location after moving file into `data/chart`
	from .data.chart.plot_compressed_trading_chart import plot_compressed_trading_chart  # type: ignore
except Exception:
	# fallback for environments that still reference the old path
	from .data.plot_compressed_trading_chart import plot_compressed_trading_chart  # type: ignore

__all__ = [
	"plot_compressed_trading_chart",
]
