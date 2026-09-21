# Computer Runtime Checkpoint

## Date
2026-09-21

## Purpose
Bootstrap a local Windows runtime for the XAUUSD forward-shadow development path using Equiti Demo + MetaTrader 5. cTrader is intentionally not part of the current runtime path.

## Current runtime
- OS: Windows
- Python: 3.11.0
- Git: 2.55.0.windows.3
- Python virtual environment: `.venv`
- MT5 Python package: installed and importable
- Broker: Equiti Brokerage (Seychelles) Limited
- Server: `EquitiBrokerageSC-Demo`
- XAUUSD symbol: `XAUUSD.sd`
- Trading: no orders submitted; connectivity and data tests are read-only

## Completed
1. Repository cloned successfully.
2. Repository verified on `main`, synchronized with `origin/main`.
3. Python virtual environment created and activated.
4. Python version verified.
5. `MetaTrader5` Python package installed and imported successfully.
6. MT5 initialization test succeeded:
   - `mt5.initialize()` -> `True`
   - `mt5.last_error()` -> `(1, 'Success')`
   - `mt5.shutdown()` executed.
7. Read-only Equiti account probe succeeded:
   - Connected: `True`
   - Account login: `1059868`
   - Broker: Equiti Brokerage (Seychelles) Limited
   - Server: `EquitiBrokerageSC-Demo`
   - Account trade mode: `0`
   - Currency: USD
8. `XAUUSD.sd` market-data access succeeded:
   - Symbol description: Gold vs US Dollar
   - Digits: 2
   - Point: 0.01
   - Live forward tick Bid/Ask was readable
   - Recent bars were readable on M1, M5, M15, M30, H1, H4
9. No trading order has been submitted.
10. Read-only `MT5MarketDataAdapter` implemented at `src/xauusd_intelligence/mt5_market_data.py`.
11. Adapter contract tests added at `tests/test_mt5_market_data.py`.
12. The adapter uses dependency injection for the MT5 module so tests do not require a live terminal.

## Current milestone
**MT5 -> Forward Shadow observation builder: IMPLEMENTED / UNIT TESTS PASSED**

A read-only MT5 snapshot can now be converted into the existing immutable forward-shadow observation contract. The observation timestamp comes from the observed MT5 tick, and its identity/digest are derived only from the snapshot. No outcome data, order submission, or position management is involved.

## Read-only / causality boundary
The probe, MT5 adapter, and observation builder only initialize/connect to MT5 and read/normalize market data. They do not submit orders or modify positions. The observation builder does not calculate or attach outcomes and does not have access to future market data.

## Next step
Unit tests passed locally: `9 passed in 0.27s`. Next, run a real local MT5 smoke test that captures one current `XAUUSD.sd` snapshot and converts it into a forward-shadow observation without submitting any order.

The implementation must preserve:
- no order submission
- no live-position management
- no strategy hard-coding
- no future-data leakage
- GitHub checkpoint after each meaningful milestone

Master Plan changes require explicit user approval.
