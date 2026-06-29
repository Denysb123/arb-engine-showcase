"""
Encryption of secrets (e.g. API keys) for storage at rest in a database.

The Fernet key is resolved from, in order:
  1) the ARB_SECRET env var (url-safe base64, 32 bytes) — used on the server;
  2) a local `secret.key` file next to the app (auto-created on first run).

An `enc:` marker distinguishes encrypted values from legacy plaintext, so an
existing database keeps working while new/re-saved values are encrypted.
"""
import os

from cryptography.fernet import Fernet, InvalidToken

_PREFIX = "enc:"
_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secret.key")


def _load_key() -> bytes:
    env = os.environ.get("ARB_SECRET", "").strip()
    if env:
        return env.encode()
    if os.path.exists(_KEY_FILE):
        with open(_KEY_FILE, "rb") as f:
            return f.read().strip()
    # first run — generate and persist a key
    key = Fernet.generate_key()
    with open(_KEY_FILE, "wb") as f:
        f.write(key)
    try:
        os.chmod(_KEY_FILE, 0o600)  # no-op on Windows, but useful on Linux/VPS
    except OSError:
        pass
    return key


_FERNET = Fernet(_load_key())


def enc(plaintext: str) -> str:
    """Encrypt a string. Empty -> empty. Already encrypted -> unchanged."""
    if not plaintext:
        return ""
    if plaintext.startswith(_PREFIX):
        return plaintext
    token = _FERNET.encrypt(plaintext.encode()).decode()
    return _PREFIX + token


def dec(value: str) -> str:
    """Decrypt a value. Legacy plaintext (no marker) is returned as-is."""
    if not value:
        return ""
    if not value.startswith(_PREFIX):
        return value  # legacy plaintext
    token = value[len(_PREFIX):]
    try:
        return _FERNET.decrypt(token.encode()).decode()
    except InvalidToken:
        # wrong/rotated key — fail loud rather than returning garbage
        raise ValueError("Could not decrypt value: invalid key or corrupt data")
