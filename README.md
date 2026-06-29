# arb-engine-showcase

A curated, sanitized showcase of engineering patterns I use when building
**async trading / arbitrage infrastructure in Python**.

> ⚠️ This repository intentionally **does not** contain any live trading
> strategy, exchange credentials, or production data. It is a portfolio
> sample that demonstrates code quality, structure and engineering practices —
> the proprietary parts of my projects are kept private.

---

## What this demonstrates

| Area | File | What it shows |
|------|------|----------------|
| 🔐 Secret encryption | [`src/crypto.py`](src/crypto.py) | Fernet-based encryption for storing API keys at rest, with env/file key loading and backward compatibility |
| 🛠️ Exchange abstraction | [`src/exchanges.py`](src/exchanges.py) | Normalizing symbol formats and instrument metadata across multiple exchanges (Binance, Bybit, MEXC, Gate, BingX) |
| ⚡ Caching | [`src/cache.py`](src/cache.py) | A small TTL cache decorator for rate-limit-friendly access to public endpoints |
| 🔏 Signed REST | [`src/signed_request.py`](src/signed_request.py) | Async HMAC-SHA256 signed requests to private exchange endpoints, with the secret never sent over the wire |
| 🗃️ Data layer | [`src/models.py`](src/models.py) | Clean `dataclass`-based domain models for trades and positions |
| ✅ Tests | [`tests/`](tests/) | `pytest` coverage for the encryption and exchange utilities |

---

## Architecture (high level)

The real project is a multi-exchange arbitrage / funding terminal built around
an async core. At a high level:

```
            ┌────────────────────┐
            │   Web dashboard     │   live PnL, positions, controls
            └─────────┬──────────┘
                      │  HTTP / WebSocket
            ┌─────────▼──────────┐
            │     Async core      │   asyncio event loop
            │  ┌──────────────┐   │
            │  │ Trading engine│  │   open/close logic, spread tracking
            │  └──────┬───────┘   │
            │         │            │
            │  ┌──────▼───────┐   │
            │  │ Exchange API  │  │   signed REST, instrument cache
            │  │   adapters    │  │
            │  └──────┬───────┘   │
            └─────────┼──────────┘
                      │
            ┌─────────▼──────────┐
            │   SQLite storage    │   trades, positions, encrypted keys
            └────────────────────┘
```

**Engineering principles I follow:**

- Secrets are **encrypted at rest** and never committed — keys come from env
  vars (`ARB_SECRET`) on the server or a gitignored local key file.
- Exchange differences (symbol format, volume step, contract size) are isolated
  behind small adapters so the core logic stays exchange-agnostic.
- Public endpoints are **cached with a TTL** to respect rate limits.
- Domain objects are plain `dataclass`es — easy to test, serialize and reason about.

---

## Running the examples

```bash
pip install -r requirements.txt
pytest -q
```

## License

MIT — see [LICENSE](LICENSE).
