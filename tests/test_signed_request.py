import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from signed_request import sign, build_signed_query  # noqa: E402


def test_sign_is_deterministic():
    a = sign("secret", "symbol=BTCUSDT&timestamp=1")
    b = sign("secret", "symbol=BTCUSDT&timestamp=1")
    assert a == b
    assert len(a) == 64  # hex sha256


def test_sign_changes_with_secret():
    assert sign("s1", "x=1") != sign("s2", "x=1")


def test_build_signed_query_appends_signature_and_timestamp():
    query = build_signed_query("api-secret", {"symbol": "BTCUSDT"})
    assert "symbol=BTCUSDT" in query
    assert "timestamp=" in query
    assert "&signature=" in query
    # signature must be the last parameter (covers everything before it)
    assert query.index("signature") > query.index("timestamp")
