"""
Domain models.

Plain `dataclass`es for the core trading entities. Keeping these as simple,
serializable value objects makes them easy to store, test and reason about.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Trade:
    """A completed or in-progress trade between two venues (e1, e2)."""
    symbol: str
    e1: str
    e2: str
    side: str
    qty: float
    entry_spread: float
    open_time: str
    close_time: Optional[str] = None
    exit_spread: Optional[float] = None
    realized_pnl: float = 0.0
    funding_fee: float = 0.0

    @property
    def is_open(self) -> bool:
        return self.close_time is None


@dataclass
class Position:
    """A currently held position on a single venue."""
    symbol: str
    exchange: str
    side: str
    qty: float
    entry_price: float
    tags: list = field(default_factory=list)

    def notional(self) -> float:
        """Position value in quote currency."""
        return self.qty * self.entry_price
