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
- Broker: Equiti Demo
- XAUUSD symbol: `XAUUSD.sd`
- Trading: disabled; connectivity tests are read-only

## Completed
1. Repository cloned successfully.
2. Repository verified on `main`, synchronized with `origin/main`, working tree clean.
3. Python virtual environment created and activated.
4. Python version verified.
5. `MetaTrader5` Python package installed and imported successfully.
6. MT5 initialization test succeeded:
   - `mt5.initialize()` -> `True`
   - `mt5.last_error()` -> `(1, 'Success')`
   - `mt5.shutdown()` executed.
7. No trading order has been submitted.

## Current milestone
**Python -> MT5 process connectivity: PASSED**

This proves that Python can initialize the local MetaTrader 5 terminal. It does not yet prove that the intended Equiti account, server, or `XAUUSD.sd` market data can be read successfully.

## Next step
Run a read-only account/symbol/data probe to verify:
- connected Equiti account and server
- account is Demo
- `XAUUSD.sd` exists and is selectable
- current tick Bid/Ask
- recent candles for the required timeframes

No order submission is permitted during this bootstrap phase.
