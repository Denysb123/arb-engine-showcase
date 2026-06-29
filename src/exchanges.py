"""
Exchange abstraction helpers.

Different exchanges use different symbol formats and instrument metadata.
These helpers normalize those differences so the rest of the codebase can stay
exchange-agnostic. Only public, non-sensitive conventions are included here.
"""
from dataclasses import dataclass


def fmt_symbol(exchange: str, base: str) -> str:
    """Convert a base asset (e.g. 'BTC') into the symbol format an exchange expects.

    >>> fmt_symbol("binance", "BTC")
    'BTCUSDT'
    >>> fmt_symbol("mexc", "ETH")
    'ETH_USDT'
    >>> fmt_symbol("bingx", "sol")
    'SOL-USDT'
    """
    base = base.strip().upper().replace("USDT", "").replace("_", "").replace("-", "")
    ex = exchange.upper()
    if ex in ("MEXC", "GATE", "GATEIO"):
        return f"{base}_USDT"
    if ex == "BINGX":
        return f"{base}-USDT"
    return f"{base}USDT"  # BINANCE, BYBIT and most others


@dataclass(frozen=True)
class InstrumentInfo:
    """Trading constraints for a single instrument on a given exchange."""
    symbol: str
    qty_step: float        # smallest increment of order size
    min_qty: float         # minimum order size
    contract_size: float = 1.0


def round_to_step(qty: float, step: float) -> float:
    """Round an order size down to a valid multiple of the exchange's qty step.

    Exchanges reject orders whose size isn't a multiple of `qty_step`, so any
    computed position size has to be snapped to the grid before submission.

    >>> round_to_step(1.2345, 0.001)
    1.234
    >>> round_to_step(7.9, 0.5)
    7.5
    """
    if step <= 0:
        return qty
    steps = int(qty / step)
    return round(steps * step, 10)
