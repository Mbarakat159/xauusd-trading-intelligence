from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json

VERSION = "decision-risk-execution-safety-v1.0.0"

class SafetyDisposition(str, Enum):
    ALLOW = "ALLOW"
    WAIT = "WAIT"
    BLOCK = "BLOCK"

class ToolHealth(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"

class PositionState(str, Enum):
    FLAT = "FLAT"
    OPEN = "OPEN"
    EXIT_PENDING = "EXIT_PENDING"
    EXITED = "EXITED"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class SafetyLimits:
    max_spread: float
    max_quote_age_seconds: float
    max_slippage: float
    max_gross_exposure: float
    max_net_exposure: float
    max_open_positions: int
    max_data_age_seconds: float
    max_watchdog_gap_seconds: float

@dataclass(frozen=True)
class SafetyInput:
    as_of: datetime
    upstream_action: str
    quote_ts: datetime | None
    bid: float | None
    ask: float | None
    expected_price: float | None
    requested_exposure: float
    current_gross_exposure: float
    current_net_exposure: float
    current_open_positions: int
    data_age_seconds: float
    tool_health: ToolHealth
    watchdog_gap_seconds: float
    kill_switch_active: bool
    position_state: PositionState

@dataclass(frozen=True)
class SafetyDecision:
    as_of: datetime
    version: str
    disposition: SafetyDisposition
    reasons: tuple[str, ...]
    constraints_checked: tuple[str, ...]
    immutable_input_digest: str

@dataclass(frozen=True)
class WatchdogState:
    as_of: datetime
    last_heartbeat: datetime | None
    max_gap_seconds: float
    kill_switch_active: bool
    latched: bool

@dataclass(frozen=True)
class WatchdogDecision:
    healthy: bool
    kill_switch_required: bool
    reasons: tuple[str, ...]
    version: str = VERSION

@dataclass(frozen=True)
class PositionSnapshot:
    as_of: datetime
    state: PositionState
    broker_position_id: str | None
    quantity: float
    average_price: float | None
    source: str

@dataclass(frozen=True)
class PositionTransition:
    allowed: bool
    from_state: PositionState
    to_state: PositionState
    reason: str

@dataclass(frozen=True)
class RollbackRecord:
    active_version: str
    last_known_good_version: str
    rollback_allowed: bool
    reason: str

def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("naive timestamp is not allowed")
    return dt.astimezone(timezone.utc)

def _digest(inp: SafetyInput) -> str:
    payload = {
        "as_of": _utc(inp.as_of).isoformat(),
        "upstream_action": inp.upstream_action,
        "quote_ts": None if inp.quote_ts is None else _utc(inp.quote_ts).isoformat(),
        "bid": inp.bid, "ask": inp.ask, "expected_price": inp.expected_price,
        "requested_exposure": inp.requested_exposure,
        "current_gross_exposure": inp.current_gross_exposure,
        "current_net_exposure": inp.current_net_exposure,
        "current_open_positions": inp.current_open_positions,
        "data_age_seconds": inp.data_age_seconds,
        "tool_health": inp.tool_health.value,
        "watchdog_gap_seconds": inp.watchdog_gap_seconds,
        "kill_switch_active": inp.kill_switch_active,
        "position_state": inp.position_state.value,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode()).hexdigest()

def evaluate_safety(inp: SafetyInput, limits: SafetyLimits) -> SafetyDecision:
    """Deterministic fail-closed safety gate.
    It never chooses direction, entry, target, stop, strategy, or position size.
    """
    as_of = _utc(inp.as_of)
    reasons: list[str] = []
    hard_failures: list[str] = []
    soft_waits: list[str] = []
    checked = (
        "kill_switch", "tool_health", "quote_freshness", "quote_integrity",
        "spread", "slippage", "data_freshness", "gross_exposure",
        "net_exposure", "open_position_count", "watchdog",
    )
    if inp.kill_switch_active:
        reasons.append("kill switch active")
        hard_failures.append("kill switch active")
    if inp.tool_health != ToolHealth.HEALTHY:
        reasons.append("required tool health is not HEALTHY")
        (hard_failures if inp.tool_health == ToolHealth.FAILED else soft_waits).append("required tool health is not HEALTHY")
    if inp.quote_ts is None or (as_of - _utc(inp.quote_ts)).total_seconds() > limits.max_quote_age_seconds:
        reasons.append("quote is missing or stale")
        soft_waits.append("quote is missing or stale")
    if inp.bid is None or inp.ask is None or inp.ask < inp.bid:
        reasons.append("quote is missing or invalid")
        hard_failures.append("quote is missing or invalid")
    elif inp.ask - inp.bid > limits.max_spread:
        reasons.append("spread exceeds hard limit")
        hard_failures.append("spread exceeds hard limit")
    if inp.expected_price is None:
        reasons.append("expected execution price is unavailable")
        soft_waits.append("expected execution price is unavailable")
    elif inp.bid is not None and inp.ask is not None:
        reference = (inp.bid + inp.ask) / 2.0
        if abs(inp.expected_price - reference) > limits.max_slippage:
            reasons.append("expected execution deviation exceeds hard limit")
            hard_failures.append("expected execution deviation exceeds hard limit")
    if inp.data_age_seconds > limits.max_data_age_seconds:
        reasons.append("data exceeds freshness limit")
        soft_waits.append("data exceeds freshness limit")
    if inp.current_gross_exposure + max(inp.requested_exposure, 0.0) > limits.max_gross_exposure:
        reasons.append("gross exposure limit would be exceeded")
        hard_failures.append("gross exposure limit would be exceeded")
    if abs(inp.current_net_exposure + inp.requested_exposure) > limits.max_net_exposure:
        reasons.append("net exposure limit would be exceeded")
        hard_failures.append("net exposure limit would be exceeded")
    if inp.current_open_positions >= limits.max_open_positions and inp.requested_exposure > 0:
        reasons.append("open-position count limit would be exceeded")
        hard_failures.append("open-position count limit would be exceeded")
    if inp.watchdog_gap_seconds > limits.max_watchdog_gap_seconds:
        reasons.append("watchdog heartbeat gap exceeds limit")
        hard_failures.append("watchdog heartbeat gap exceeds limit")
    if inp.position_state == PositionState.UNKNOWN:
        reasons.append("position state is unknown")
        hard_failures.append("position state is unknown")

    if hard_failures:\n        disposition = SafetyDisposition.BLOCK\n    elif soft_waits:\n        disposition = SafetyDisposition.WAIT\n    else:\n        disposition = SafetyDisposition.ALLOW
    return SafetyDecision(as_of, VERSION, disposition, tuple(reasons), checked, _digest(inp))

def evaluate_watchdog(state: WatchdogState) -> WatchdogDecision:
    now = _utc(state.as_of)
    if state.kill_switch_active or state.latched:
        return WatchdogDecision(False, True, ("kill switch/latch active",))
    if state.last_heartbeat is None:
        return WatchdogDecision(False, True, ("heartbeat unavailable",))
    gap = (now - _utc(state.last_heartbeat)).total_seconds()
    if gap < 0:
        raise ValueError("future heartbeat is not allowed")
    if gap > state.max_gap_seconds:
        return WatchdogDecision(False, True, ("heartbeat gap exceeds limit",))
    return WatchdogDecision(True, False, ())

def transition_position(current: PositionSnapshot, observed: PositionSnapshot) -> PositionTransition:
    allowed = {
        PositionState.FLAT: {PositionState.FLAT, PositionState.OPEN},
        PositionState.OPEN: {PositionState.OPEN, PositionState.EXIT_PENDING, PositionState.EXITED, PositionState.UNKNOWN},
        PositionState.EXIT_PENDING: {PositionState.EXIT_PENDING, PositionState.EXITED, PositionState.OPEN, PositionState.UNKNOWN},
        PositionState.EXITED: {PositionState.EXITED, PositionState.OPEN},
        PositionState.UNKNOWN: {PositionState.UNKNOWN, PositionState.FLAT, PositionState.OPEN},
    }
    if observed.as_of < current.as_of:
        return PositionTransition(False, current.state, observed.state, "observed position state is older than current state")
    ok = observed.state in allowed[current.state]
    return PositionTransition(ok, current.state, observed.state, "state transition accepted" if ok else "state transition rejected")

def rollback(record: RollbackRecord) -> RollbackRecord:
    if not record.active_version or not record.last_known_good_version:
        raise ValueError("both active and last-known-good versions are required")
    if record.active_version == record.last_known_good_version:
        return RollbackRecord(record.active_version, record.last_known_good_version, False, "no rollback target differs from active version")
    return RollbackRecord(record.active_version, record.last_known_good_version, True, "rollback target is an explicitly recorded last-known-good version")
