import os
import sys

# Use a fixed key so the test is deterministic and doesn't write a key file.
os.environ["ARB_SECRET"] = "h0gHhz063O1l0EYivNvCn7RJVZxAg_elIX2rnbFPjbg="

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from crypto import enc, dec, _PREFIX  # noqa: E402


def test_roundtrip():
    secret = "my-api-key-12345"
    token = enc(secret)
    assert token.startswith(_PREFIX)
    assert token != secret
    assert dec(token) == secret


def test_empty():
    assert enc("") == ""
    assert dec("") == ""


def test_idempotent_encrypt():
    token = enc("abc")
    assert enc(token) == token  # already encrypted -> unchanged


def test_legacy_plaintext_passthrough():
    # values without the marker are treated as legacy plaintext
    assert dec("legacy-plain-value") == "legacy-plain-value"
