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

## Current milestone
**Python -> MT5 -> Equiti Demo -> XAUUSD.sd read-only market data: PASSED**

This proves the local runtime can reach the intended Equiti Demo terminal and read current XAUUSD.sd tick/candle data across the required initial timeframes. It does not authorize or enable live trading.

## Read-only boundary
The probe script `tools/mt5_readonly_probe.py` only initializes MT5 and reads terminal/account/symbol/tick/bar information. It does not submit orders or modify positions.

## Next step
Build the first proper **MT5 Market Data Adapter** inside the project, using the verified local connection as its runtime source. The adapter should expose normalized read-only market observations to the intelligence stack rather than leaving connectivity as a standalone probe.

The next implementation must preserve:
- no order submission
- no live-position management
- no strategy hard-coding
- no future-data leakage
- GitHub checkpoint after the meaningful adapter milestone

Master Plan changes require explicit user approval.
