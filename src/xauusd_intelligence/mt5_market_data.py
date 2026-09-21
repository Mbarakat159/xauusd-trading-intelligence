"""Read-only MetaTrader 5 market-data adapter.

The adapter is deliberately limited to market-data reads. It does not expose
order submission, position management, or account mutation operations.

The MT5 module is injected so deterministic unit tests can run without a live
MetaTrader 5 terminal.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Protocol


class MT5Module(Protocol):
    def initialize(self) -> bool: ...
    def shutdown(self) -> None: ...
    def symbol_info(self, symbol: str) -> Any: ...
    def symbol_select(self, symbol: str, enable: bool) -> bool: ...
    def symbol_info_tick(self, symbol: str) -> Any: ...
    def copy_rates_from_pos(self, symbol: str, timeframe: int, start_pos: int, count: int) -> Any: ...


@dataclass(frozen=True)
class MarketTick:
    symbol: str
    bid: float
    ask: float
    time: datetime


@dataclass(frozen=True)
class MarketBar:
    symbol: str
    timeframe: str
    time: datetime
    open: float
    high: float
    low: float
    close: float
    tick_volume: int


@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    tick: MarketTick
    bars: Mapping[str, tuple[MarketBar, ...]]


class MT5MarketDataAdapter:
    """Read-only adapter around an already-installed MetaTrader 5 package."""

    def __init__(
        self,
        mt5: MT5Module,
        symbol: str = "XAUUSD.sd",
        timeframes: Mapping[str, int] | None = None,
    ) -> None:
        self._mt5 = mt5
        self.symbol = symbol
        self.timeframes = dict(timeframes or {})

    def connect(self) -> None:
        if not self._mt5.initialize():
            raise ConnectionError("MetaTrader 5 initialize() failed")

    def close(self) -> None:
        self._mt5.shutdown()

    def ensure_symbol(self) -> None:
        info = self._mt5.symbol_info(self.symbol)
        if info is None:
            raise LookupError(f"symbol not found: {self.symbol}")
        if not getattr(info, "visible", True):
            if not self._mt5.symbol_select(self.symbol, True):
                raise LookupError(f"symbol could not be selected: {self.symbol}")

    def read_tick(self) -> MarketTick:
        tick = self._mt5.symbol_info_tick(self.symbol)
        if tick is None:
            raise LookupError(f"no current tick available: {self.symbol}")
        if tick.bid is None or tick.ask is None or tick.time is None:
            raise ValueError(f"incomplete tick received: {self.symbol}")
        return MarketTick(
            symbol=self.symbol,
            bid=float(tick.bid),
            ask=float(tick.ask),
            time=_utc_from_epoch(int(tick.time)),
        )

    def read_bars(self, timeframe: str, mt5_timeframe: int, count: int = 100) -> tuple[MarketBar, ...]:
        if count <= 0:
            raise ValueError("count must be positive")
        rates = self._mt5.copy_rates_from_pos(self.symbol, mt5_timeframe, 0, count)
        if rates is None or len(rates) == 0:
            raise LookupError(f"no bars returned for {timeframe}")
        return tuple(
            MarketBar(
                symbol=self.symbol,
                timeframe=timeframe,
                time=_utc_from_epoch(int(row["time"])),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                tick_volume=int(row["tick_volume"]),
            )
            for row in rates
        )

    def snapshot(self, count: int = 100) -> MarketSnapshot:
        self.ensure_symbol()
        tick = self.read_tick()
        bars = {
            name: self.read_bars(name, timeframe, count)
            for name, timeframe in self.timeframes.items()
        }
        return MarketSnapshot(symbol=self.symbol, tick=tick, bars=bars)


def _utc_from_epoch(value: int) -> datetime:
    return datetime.fromtimestamp(value, tz=timezone.utc)
