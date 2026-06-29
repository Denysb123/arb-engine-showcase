"""
Signed REST requests to an exchange (async).

Most exchanges authenticate private endpoints with an HMAC-SHA256 signature
over the request parameters plus a timestamp. This module shows that pattern in
a generic, exchange-agnostic way — credentials are passed in by the caller and
never hard-coded or logged.
"""
import hashlib
import hmac
import time
from typing import Any, Mapping
from urllib.parse import urlencode

import aiohttp


def sign(secret: str, payload: str) -> str:
    """Return the hex HMAC-SHA256 signature of `payload` using `secret`."""
    return hmac.new(
        secret.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()


def build_signed_query(api_secret: str, params: Mapping[str, Any]) -> str:
    """Build a signed, URL-encoded query string with a millisecond timestamp.

    The timestamp guards against replay attacks; the signature is appended last
    so it covers every other parameter.
    """
    signed = dict(params)
    signed["timestamp"] = int(time.time() * 1000)
    query = urlencode(signed)
    signature = sign(api_secret, query)
    return f"{query}&signature={signature}"


async def signed_get(
    session: aiohttp.ClientSession,
    base_url: str,
    path: str,
    api_key: str,
    api_secret: str,
    params: Mapping[str, Any] | None = None,
    timeout: float = 10.0,
) -> Any:
    """Perform an authenticated GET request and return the parsed JSON.

    The API key travels in the header; the secret is only ever used locally to
    compute the signature and is never sent over the wire.
    """
    query = build_signed_query(api_secret, params or {})
    url = f"{base_url}{path}?{query}"
    headers = {"X-API-KEY": api_key}

    async with session.get(
        url, headers=headers, timeout=aiohttp.ClientTimeout(total=timeout)
    ) as resp:
        resp.raise_for_status()
        return await resp.json()
