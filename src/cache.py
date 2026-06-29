"""
A tiny TTL cache decorator.

Public exchange endpoints (instrument metadata, etc.) change rarely but are
rate-limited, so caching their results for a short window avoids hammering the
API while keeping data fresh enough.
"""
import functools
import time
from typing import Callable


def ttl_cache(seconds: float) -> Callable:
    """Cache a function's result per-arguments for `seconds`.

    >>> calls = {"n": 0}
    >>> @ttl_cache(60)
    ... def fetch(symbol):
    ...     calls["n"] += 1
    ...     return symbol.upper()
    >>> fetch("btc"), fetch("btc"), calls["n"]
    ('BTC', 'BTC', 1)
    """
    def decorator(func: Callable) -> Callable:
        store: dict = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in store:
                value, ts = store[key]
                if now - ts < seconds:
                    return value
            value = func(*args, **kwargs)
            store[key] = (value, now)
            return value

        wrapper.cache_clear = store.clear  # type: ignore[attr-defined]
        return wrapper

    return decorator
