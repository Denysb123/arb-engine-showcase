import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from exchanges import fmt_symbol, round_to_step  # noqa: E402


def test_fmt_symbol_default():
    assert fmt_symbol("binance", "BTC") == "BTCUSDT"
    assert fmt_symbol("bybit", "eth") == "ETHUSDT"


def test_fmt_symbol_underscore_exchanges():
    assert fmt_symbol("mexc", "BTC") == "BTC_USDT"
    assert fmt_symbol("gate", "sol") == "SOL_USDT"


def test_fmt_symbol_dash_exchange():
    assert fmt_symbol("bingx", "BTC") == "BTC-USDT"


def test_fmt_symbol_strips_suffix():
    assert fmt_symbol("binance", "BTCUSDT") == "BTCUSDT"


def test_round_to_step():
    assert round_to_step(1.2345, 0.001) == 1.234
    assert round_to_step(7.9, 0.5) == 7.5
    assert round_to_step(5.0, 0) == 5.0  # guard against zero step
