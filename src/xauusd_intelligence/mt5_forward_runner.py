"""Real MT5 forward-shadow capture runner.

This module is observation-only. It connects to an already-running MetaTrader 5
terminal, captures current market snapshots, freezes the Stage-7 version
contract for the session, and appends immutable observations to JSONL.

It never submits orders, reads positions, or uses future/outcome data.
"""

from __future__ import annotations

import argparse
import json
import time
import uuid
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

from .features import VERSION as FEATURE_VERSION
from .forward_capture import ForwardCapture, ForwardWindow, FrozenVersions
from .mt5_forward_observation import build_shadow_observation
from .mt5_market_data import MT5MarketDataAdapter
from .reasoning import VERSION as REASONING_VERSION
from .safety import VERSION as SAFETY_VERSION

VERSION = "mt5-forward-runner-v1.0.0"
DEFAULT_SOURCE = "MetaTrader5"
DEFAULT_VENUE = "EquitiBrokerageSC-Demo"
DEFAULT_SYMBOL = "XAUUSD.sd"


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("naive timestamp is not allowed")
    return dt.astimezone(timezone.utc)


def _json_default(value: object) -> object:
    if isinstance(value, datetime):
        return _utc(value).isoformat()
    raise TypeError(f"unsupported JSON value: {type(value)!r}")


def observation_record(observation) -> dict[str, object]:
    return asdict(observation)


class ForwardRunner:
    """Bounded or continuous real-market observation loop."""

    def __init__(
        self,
        adapter: MT5MarketDataAdapter,
        *,
        output_path: str | Path,
        symbol: str,
        source: str,
        venue: str | None,
        interval_seconds: float = 5.0,
        bar_count: int = 100,
        now: Callable[[], datetime] | None = None,
        sleep: Callable[[float], None] | None = None,
        reconnect_delay_seconds: float = 5.0,
    ) -> None:
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be positive")
        if bar_count <= 0:
            raise ValueError("bar_count must be positive")
        if reconnect_delay_seconds <= 0:
            raise ValueError("reconnect_delay_seconds must be positive")
        self.adapter = adapter
        self.output_path = Path(output_path)
        self.symbol = symbol
        self.source = source
        self.venue = venue
        self.interval_seconds = interval_seconds
        self.bar_count = bar_count
        self.reconnect_delay_seconds = reconnect_delay_seconds
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._sleep = sleep or time.sleep

    def _write_record(self, stream, record: dict[str, object]) -> None:
        stream.write(json.dumps(record, sort_keys=True, default=_json_default) + "\n")
        stream.flush()

    def run(
        self,
        *,
        max_observations: int | None = None,
        duration_seconds: float | None = None,
    ) -> int:
        if max_observations is not None and max_observations <= 0:
            raise ValueError("max_observations must be positive")
        if duration_seconds is not None and duration_seconds <= 0:
            raise ValueError("duration_seconds must be positive")

        started_at = _utc(self._now())
        versions = FrozenVersions(
            feature_version=FEATURE_VERSION,
            reasoning_version=REASONING_VERSION,
            safety_version=SAFETY_VERSION,
        )
        window = ForwardWindow(
            window_id=f"forward:{started_at.isoformat()}:{uuid.uuid4().hex[:12]}",
            symbol=self.symbol,
            source=self.source,
            venue=self.venue,
            started_at=started_at,
            versions=versions,
        )
        capture = ForwardCapture(window)
        deadline = (
            None
            if duration_seconds is None
            else started_at + timedelta(seconds=duration_seconds)
        )
        count = 0

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.adapter.connect()
        try:
            with self.output_path.open("a", encoding="utf-8") as stream:
                while True:
                    if max_observations is not None and count >= max_observations:
                        break
                    if deadline is not None and _utc(self._now()) >= deadline:
                        break

                    try:
                        snapshot = self.adapter.snapshot(count=self.bar_count)
                        if snapshot.symbol != self.symbol:
                            raise ValueError("adapter returned an unexpected symbol")

                        observation = build_shadow_observation(
                            snapshot,
                            source=self.source,
                            venue=self.venue,
                            feature_version=versions.feature_version,
                            reasoning_version=versions.reasoning_version,
                            safety_version=versions.safety_version,
                        )
                        capture.record_observation(observation)
                        self._write_record(
                            stream,
                            {
                                "record_type": "shadow_observation",
                                "runner_version": VERSION,
                                "window_id": window.window_id,
                                "captured_at": _utc(self._now()).isoformat(),
                                "observation": observation_record(observation),
                            },
                        )
                        count += 1
                    except (ConnectionError, LookupError, OSError, RuntimeError, ValueError) as exc:
                        # A source failure is recorded as a runtime event, never
                        # converted into a synthetic market observation.
                        self._write_record(
                            stream,
                            {
                                "record_type": "source_error",
                                "runner_version": VERSION,
                                "window_id": window.window_id,
                                "captured_at": _utc(self._now()).isoformat(),
                                "error_type": type(exc).__name__,
                                "error": str(exc),
                            },
                        )
                        try:
                            self.adapter.close()
                        finally:
                            if deadline is not None and _utc(self._now()) >= deadline:
                                break
                            self._sleep(self.reconnect_delay_seconds)
                            self.adapter.connect()

                    if max_observations is not None and count >= max_observations:
                        break
                    if deadline is not None and _utc(self._now()) >= deadline:
                        break
                    self._sleep(self.interval_seconds)
        finally:
            self.adapter.close()

        return count


def _build_mt5_adapter(symbol: str) -> MT5MarketDataAdapter:
    import MetaTrader5 as mt5

    timeframes = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
    }
    return MT5MarketDataAdapter(mt5, symbol=symbol, timeframes=timeframes)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run read-only XAUUSD MT5 forward-shadow capture."
    )
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    parser.add_argument("--venue", default=DEFAULT_VENUE)
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--output", default="runtime/forward_shadow/observations.jsonl")
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--bars", type=int, default=100)
    parser.add_argument("--count", type=int, default=None)
    parser.add_argument("--duration", type=float, default=None)
    args = parser.parse_args()

    runner = ForwardRunner(
        _build_mt5_adapter(args.symbol),
        output_path=args.output,
        symbol=args.symbol,
        source=args.source,
        venue=args.venue,
        interval_seconds=args.interval,
        bar_count=args.bars,
    )
    count = runner.run(
        max_observations=args.count,
        duration_seconds=args.duration,
    )
    print(
        f"forward-shadow capture complete: observations={count} "
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
