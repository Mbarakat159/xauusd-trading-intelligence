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
**MT5 -> Forward Shadow observation builder: REAL MT5 SMOKE TEST PASSED**

A real local MT5 snapshot from `XAUUSD.sd` was successfully converted into the immutable forward-shadow observation contract.

Smoke-test result:
- Snapshot: **OK**
- Symbol: `XAUUSD.sd`
- Forward tick: Bid `4350.26`, Ask `4350.53`
- Observation time: `2026-09-21T19:28:07+00:00`
- Timeframes captured: M1, M5, M15, M30, H1, H4
- Bars per timeframe: 20
- Observation: **OK**
- Observation ID: `mt5:XAUUSD.sd:2026-09-21T19:28:07+00:00:2c13608977e3f768`
- Payload digest: `2c13608977e3f768018d60c007b0e47f418982fb95d3f06da08104b95bdf640b`
- No order was submitted.

## Read-only / causality boundary
The probe, MT5 adapter, and observation builder only initialize/connect to MT5 and read/normalize market data. They do not submit orders or modify positions. The observation builder does not calculate or attach outcomes and does not have access to future market data.

## Next step
The local MT5 -> forward-shadow data path is now proven end-to-end for a real current observation. Next, implement the **forward capture session/loop** that records repeated real observations under one frozen Stage 7 version contract, still with no orders and no online self-modification.

The implementation must preserve:
- no order submission
- no live-position management
- no strategy hard-coding
- no future-data leakage
- GitHub checkpoint after each meaningful milestone

Master Plan changes require explicit user approval.
