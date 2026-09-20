from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from math import sqrt
from statistics import pstdev
from typing import Any, Iterable

VERSION = "deterministic-features-v1.0.0"

class Quality(str, Enum):
    VALID = "VALID"
    STALE = "STALE"
    MISSING = "MISSING"
    CONFLICTING = "CONFLICTING"
    INVALID = "INVALID"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class Result:
    feature: str
    value: Any
    quality: Quality
    as_of: datetime
    version: str = VERSION
    reason: str | None = None

@dataclass(frozen=True)
class Bar:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    source: str = "unknown"
    venue: str | None = None
    timeframe: str = "unknown"
    arrival_ts: datetime | None = None
    quality: Quality = Quality.VALID

@dataclass(frozen=True)
class Quote:
    ts: datetime
    bid: float | None
    ask: float | None
    source: str
    quality: Quality = Quality.VALID

@dataclass(frozen=True)
class Event:
    ts: datetime
    name: str
    timezone_name: str = "UTC"

@dataclass(frozen=True)
class Config:
    version: str = VERSION
    swing_left: int = 2
    swing_right: int = 2
    volatility_window: int = 5
    volatility_baseline_window: int = 10
    range_window: int = 10
    break_buffer: float = 0.0
    spread_max_age_seconds: int = 5
    event_pre_seconds: int = 900
    event_post_seconds: int = 900

def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("naive timestamp is not allowed")
    return dt.astimezone(timezone.utc)

def _valid_bars(bars: Iterable[Bar], cutoff: datetime) -> list[Bar]:
    c = _utc(cutoff)
    out = [b for b in bars if _utc(b.ts) <= c]
    out.sort(key=lambda b: _utc(b.ts))
    return out

def _result(name: str, value: Any, quality: Quality, cutoff: datetime, reason: str | None = None) -> Result:
    return Result(name, value, quality, _utc(cutoff), reason=reason)

def f001_ohlc_geometry(bar: Bar, cutoff: datetime) -> Result:
    c = _utc(cutoff)
    if _utc(bar.ts) > c or bar.quality != Quality.VALID:
        return _result("F001", None, bar.quality, c, "bar unavailable/invalid at cutoff")
    ok = bar.high >= max(bar.open, bar.close) and bar.low <= min(bar.open, bar.close) and bar.high >= bar.low
    return _result("F001", ok, Quality.VALID if ok else Quality.INVALID, c, None if ok else "OHLC invariant violated")

def f002_returns(bars: Iterable[Bar], cutoff: datetime) -> Result:
    bs = _valid_bars(bars, cutoff); c = _utc(cutoff)
    if len(bs) < 2 or bs[-1].quality != Quality.VALID or bs[-2].quality != Quality.VALID:
        return _result("F002", None, Quality.UNKNOWN, c, "valid previous close unavailable")
    return _result("F002", bs[-1].close / bs[-2].close - 1.0, Quality.VALID, c)

def f003_true_range(bars: Iterable[Bar], cutoff: datetime) -> Result:
    bs = _valid_bars(bars, cutoff); c = _utc(cutoff)
    if len(bs) < 2 or any(b.quality != Quality.VALID for b in bs[-2:]):
        return _result("F003", None, Quality.UNKNOWN, c, "previous valid close unavailable")
    b, prev = bs[-1], bs[-2]
    return _result("F003", max(b.high - b.low, abs(b.high - prev.close), abs(b.low - prev.close)), Quality.VALID, c)

def f004_realized_volatility(bars: Iterable[Bar], cutoff: datetime, window: int) -> Result:
    bs = _valid_bars(bars, cutoff); c = _utc(cutoff)
    if window < 2 or len(bs) < window + 1:
        return _result("F004", None, Quality.UNKNOWN, c, "insufficient causal returns")
    closes = [b.close for b in bs[-window-1:]]
    rs = [closes[i] / closes[i-1] - 1.0 for i in range(1, len(closes))]
    return _result("F004", pstdev(rs) * sqrt(window), Quality.VALID, c)

def f005_volatility_baseline(bars: Iterable[Bar], cutoff: datetime, vol_window: int, baseline_window: int) -> Result:
    bs = _valid_bars(bars, cutoff); c = _utc(cutoff)
    if baseline_window < 1 or len(bs) < baseline_window + vol_window:
        return _result("F005", None, Quality.UNKNOWN, c, "insufficient causal baseline")
    vols = []
    for i in range(vol_window, len(bs) + 1):
        chunk = bs[:i]
        r = f004_realized_volatility(chunk, chunk[-1].ts, vol_window)
        if r.quality == Quality.VALID:
            vols.append(r.value)
    if len(vols) < baseline_window:
        return _result("F005", None, Quality.UNKNOWN, c, "insufficient baseline observations")
    return _result("F005", {"current": vols[-1], "baseline": pstdev(vols[-baseline_window:]) if baseline_window > 1 else 0.0}, Quality.VALID, c)

def f006_range_position(bars: Iterable[Bar], cutoff: datetime, window: int) -> Result:
    bs = _valid_bars(bars, cutoff); c = _utc(cutoff)
    if not bs or len(bs) < window:
        return _result("F006", None, Quality.UNKNOWN, c, "range undefined")
    ref = bs[-window:]; hi = max(b.high for b in ref); lo = min(b.low for b in ref)
    if hi == lo:
        return _result("F006", None, Quality.UNKNOWN, c, "zero-width range")
    return _result("F006", (bs[-1].close - lo) / (hi - lo), Quality.VALID, c)

def _confirmed_swings(bars: list[Bar], left: int, right: int) -> list[tuple[datetime, str, float, datetime]]:
    out = []
    for i in range(left, len(bars) - right):
        w = bars[i-left:i+right+1]; b = bars[i]
        if any(x.quality != Quality.VALID for x in w):
            continue
        if b.high == max(x.high for x in w) and sum(x.high == b.high for x in w) == 1:
            out.append((b.ts, "HIGH", b.high, bars[i+right].ts))
        if b.low == min(x.low for x in w) and sum(x.low == b.low for x in w) == 1:
            out.append((b.ts, "LOW", b.low, bars[i+right].ts))
    return out

def f007_confirmed_swing(bars: Iterable[Bar], cutoff: datetime, left: int, right: int) -> Result:
    bs = _valid_bars(bars, cutoff); c = _utc(cutoff)
    swings = [x for x in _confirmed_swings(bs, left, right) if _utc(x[3]) <= c]
    if not swings:
        return _result("F007", None, Quality.UNKNOWN, c, "no confirmed swing available")
    x = sorted(swings, key=lambda z: _utc(z[3]))[-1]
    return _result("F007", {"pivot_ts": _utc(x[0]).isoformat(), "kind": x[1], "price": x[2], "confirmed_ts": _utc(x[3]).isoformat()}, Quality.VALID, c)

def f008_structural_reference(bars: Iterable[Bar], cutoff: datetime, left: int, right: int) -> Result:
    r = f007_confirmed_swing(bars, cutoff, left, right)
    value = None if r.value is None else {"price": r.value["price"], "kind": r.value["kind"], "confirmed_ts": r.value["confirmed_ts"]}
    return _result("F008", value, r.quality, r.as_of, r.reason)

def f009_structural_break(bars: Iterable[Bar], cutoff: datetime, left: int, right: int, buffer: float = 0.0) -> Result:
    bs = _valid_bars(bars, cutoff); c = _utc(cutoff); ref = f008_structural_reference(bs, c, left, right)
    if ref.quality != Quality.VALID:
        return _result("F009", None, Quality.UNKNOWN, c, "no structural reference")
    level = ref.value["price"]; kind = ref.value["kind"]; b = bs[-1]
    broken = (kind == "HIGH" and b.close > level + buffer) or (kind == "LOW" and b.close < level - buffer)
    return _result("F009", broken, Quality.VALID, c)

def f010_structural_distance(bars: Iterable[Bar], cutoff: datetime, left: int, right: int) -> Result:
    bs = _valid_bars(bars, cutoff); c = _utc(cutoff); ref = f008_structural_reference(bs, c, left, right)
    if ref.quality != Quality.VALID:
        return _result("F010", None, Quality.UNKNOWN, c, "no structural reference")
    return _result("F010", bs[-1].close - ref.value["price"], Quality.VALID, c)

def f011_spread(quotes: Iterable[Quote], cutoff: datetime, max_age_seconds: int) -> Result:
    c = _utc(cutoff); qs = [q for q in quotes if _utc(q.ts) <= c]
    if not qs:
        return _result("F011", None, Quality.MISSING, c, "no quote")
    q = max(qs, key=lambda x: _utc(x.ts))
    if q.quality != Quality.VALID:
        return _result("F011", None, q.quality, c, "quote quality failure")
    if (c - _utc(q.ts)).total_seconds() > max_age_seconds:
        return _result("F011", None, Quality.STALE, c, "quote exceeds freshness budget")
    if q.bid is None or q.ask is None:
        return _result("F011", None, Quality.MISSING, c, "bid/ask missing")
    if q.ask < q.bid:
        return _result("F011", None, Quality.INVALID, c, "ask below bid")
    return _result("F011", q.ask - q.bid, Quality.VALID, c)

def f012_activity_proxy(count: int | None, source: str | None, cutoff: datetime) -> Result:
    c = _utc(cutoff)
    if count is None or source is None:
        return _result("F012", None, Quality.UNKNOWN, c, "activity source/count missing")
    if count < 0:
        return _result("F012", None, Quality.INVALID, c, "negative activity")
    return _result("F012", {"count": count, "source": source, "measurement": "tick_activity_proxy"}, Quality.VALID, c)

def f013_volume_provenance(*, venue: str | None, instrument: str | None, source: str | None, measurement: str | None, interval: str | None, cutoff: datetime) -> Result:
    c = _utc(cutoff); fields = [venue, instrument, source, measurement, interval]
    if any(x is None for x in fields):
        return _result("F013", None, Quality.UNKNOWN, c, "required provenance missing")
    return _result("F013", {"venue": venue, "instrument": instrument, "source": source, "measurement": measurement, "interval": interval}, Quality.VALID, c)

def f014_event_distance(now: datetime, event: Event | None) -> Result:
    c = _utc(now)
    if event is None:
        return _result("F014", None, Quality.UNKNOWN, c, "event timestamp unavailable")
    return _result("F014", (_utc(event.ts) - c).total_seconds(), Quality.VALID, c)

def f015_session_state(ts: datetime, session: str, calendar_version: str, timezone_name: str = "UTC") -> Result:
    c = _utc(ts)
    if not session or not calendar_version:
        return _result("F015", None, Quality.UNKNOWN, c, "calendar/session metadata missing")
    return _result("F015", {"session": session, "calendar_version": calendar_version, "timezone": timezone_name}, Quality.VALID, c)

def f016_mtf_synchronization(bars_by_tf: dict[str, Iterable[Bar]], cutoff: datetime) -> Result:
    c = _utc(cutoff); out = {}
    for tf, bars in bars_by_tf.items():
        bs = _valid_bars(bars, c)
        out[tf] = _utc(bs[-1].ts).isoformat() if bs else None
    if not out or any(v is None for v in out.values()):
        return _result("F016", out, Quality.UNKNOWN, c, "one or more timeframes unavailable")
    return _result("F016", out, Quality.VALID, c)

def f017_event_window(now: datetime, event: Event | None, pre_seconds: int, post_seconds: int) -> Result:
    c = _utc(now)
    if event is None:
        return _result("F017", None, Quality.UNKNOWN, c, "event unavailable")
    d = (_utc(event.ts) - c).total_seconds()
    state = "pre-event" if 0 < d <= pre_seconds else "event-window" if d == 0 else "post-event" if -post_seconds <= d < 0 else "ordinary"
    return _result("F017", state, Quality.VALID, c)

def f018_proxy_capability(claim: str, required_fields: set[str], available_fields: set[str], cutoff: datetime) -> Result:
    c = _utc(cutoff)
    if not claim:
        return _result("F018", None, Quality.UNKNOWN, c, "claim missing")
    if required_fields.issubset(available_fields):
        state = "SUFFICIENT"
    elif required_fields & available_fields:
        state = "PARTIAL"
    else:
        state = "UNKNOWN"
    return _result("F018", {"claim": claim, "capability": state}, Quality.VALID, c)
