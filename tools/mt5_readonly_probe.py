"""Read-only MT5 connectivity probe for the Equiti Demo runtime.

This script never sends trading orders. It verifies the connected terminal/account,
checks XAUUSD.sd, and reads current tick plus recent OHLCV data.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone

import MetaTrader5 as mt5


SYMBOL = "XAUUSD.sd"
TIMEFRAMES = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    print(f"MT5 last error: {mt5.last_error()}")
    mt5.shutdown()
    sys.exit(1)


if not mt5.initialize():
    fail("MT5 initialize() failed")

try:
    terminal = mt5.terminal_info()
    account = mt5.account_info()

    if terminal is None:
        fail("terminal_info() returned None")
    if account is None:
        fail("account_info() returned None")

    print("=== MT5 READ-ONLY PROBE ===")
    print(f"Terminal: {terminal.name}")
    print(f"Connected: {terminal.connected}")
    print(f"Trade allowed by terminal: {terminal.trade_allowed}")
    print(f"Account login: {account.login}")
    print(f"Broker: {account.company}")
    print(f"Server: {account.server}")
    print(f"Account trade mode: {account.trade_mode}")
    print(f"Balance: {account.balance}")
    print(f"Currency: {account.currency}")

    symbol_info = mt5.symbol_info(SYMBOL)
    if symbol_info is None:
        fail(f"symbol not found: {SYMBOL}")

    if not symbol_info.visible:
        if not mt5.symbol_select(SYMBOL, True):
            fail(f"symbol exists but could not be selected: {SYMBOL}")

    tick = mt5.symbol_info_tick(SYMBOL)
    if tick is None:
        fail(f"no current tick available for {SYMBOL}")

    print()
    print(f"Symbol: {SYMBOL}")
    print(f"Description: {symbol_info.description}")
    print(f"Digits: {symbol_info.digits}")
    print(f"Point: {symbol_info.point}")
    print(f"Bid: {tick.bid}")
    print(f"Ask: {tick.ask}")
    if tick.time:
        tick_dt = datetime.fromtimestamp(tick.time, tz=timezone.utc)
        print(f"Tick UTC: {tick_dt.isoformat()}")

    print()
    print("Recent bars:")
    for name, timeframe in TIMEFRAMES.items():
        rates = mt5.copy_rates_from_pos(SYMBOL, timeframe, 0, 3)
        if rates is None or len(rates) == 0:
            fail(f"no bars returned for {name}")

        latest = rates[-1]
        bar_dt = datetime.fromtimestamp(int(latest["time"]), tz=timezone.utc)
        print(
            f"{name}: OK | time={bar_dt.isoformat()} "
            f"open={latest['open']} high={latest['high']} "
            f"low={latest['low']} close={latest['close']} "
            f"tick_volume={latest['tick_volume']}"
        )

    print()
    print("RESULT: READ-ONLY MT5 / EQUITI / XAUUSD.sd DATA ACCESS OK")
    print("TRADING: NOT USED")
finally:
    mt5.shutdown()
