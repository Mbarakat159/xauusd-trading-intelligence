from datetime import datetime, timedelta, timezone

from xauusd_intelligence.safety import (
    PositionSnapshot, PositionState, RollbackRecord, SafetyDisposition,
    SafetyInput, SafetyLimits, ToolHealth, WatchdogState,
    evaluate_safety, evaluate_watchdog, rollback, transition_position,
)

def now():
    return datetime(2026, 9, 21, 12, tzinfo=timezone.utc)

def limits():
    return SafetyLimits(1.0, 5, 0.5, 100, 80, 3, 10, 5)

def base(**kwargs):
    values = dict(
        as_of=now(), upstream_action="TRADE", quote_ts=now(),
        bid=2500.0, ask=2500.5, expected_price=2500.25,
        requested_exposure=10, current_gross_exposure=20,
        current_net_exposure=10, current_open_positions=1,
        data_age_seconds=2, tool_health=ToolHealth.HEALTHY,
        watchdog_gap_seconds=1, kill_switch_active=False,
        position_state=PositionState.OPEN,
    )
    values.update(kwargs)
    return SafetyInput(**values)

def test_valid_request_is_allowed():
    assert evaluate_safety(base(), limits()).disposition == SafetyDisposition.ALLOW

def test_kill_switch_blocks():
    assert evaluate_safety(base(kill_switch_active=True), limits()).disposition == SafetyDisposition.BLOCK

def test_tool_failure_blocks():
    assert evaluate_safety(base(tool_health=ToolHealth.FAILED), limits()).disposition == SafetyDisposition.BLOCK

def test_stale_quote_blocks():
    assert evaluate_safety(base(quote_ts=now() - timedelta(seconds=6)), limits()).disposition == SafetyDisposition.BLOCK

def test_invalid_quote_blocks():
    assert evaluate_safety(base(ask=2499.0), limits()).disposition == SafetyDisposition.BLOCK

def test_spread_limit_blocks():
    assert evaluate_safety(base(ask=2501.1), limits()).disposition == SafetyDisposition.BLOCK

def test_slippage_limit_blocks():
    assert evaluate_safety(base(expected_price=2501.0), limits()).disposition == SafetyDisposition.BLOCK

def test_data_freshness_blocks():
    assert evaluate_safety(base(data_age_seconds=11), limits()).disposition == SafetyDisposition.BLOCK

def test_gross_exposure_blocks():
    assert evaluate_safety(base(current_gross_exposure=95), limits()).disposition == SafetyDisposition.BLOCK

def test_net_exposure_blocks():
    assert evaluate_safety(base(current_net_exposure=75), limits()).disposition == SafetyDisposition.BLOCK

def test_position_count_blocks_new_exposure():
    assert evaluate_safety(base(current_open_positions=3), limits()).disposition == SafetyDisposition.BLOCK

def test_unknown_position_state_blocks():
    assert evaluate_safety(base(position_state=PositionState.UNKNOWN), limits()).disposition == SafetyDisposition.BLOCK

def test_watchdog_gap_blocks():
    assert evaluate_safety(base(watchdog_gap_seconds=6), limits()).disposition == SafetyDisposition.BLOCK

def test_watchdog_requires_kill_switch_on_stale_heartbeat():
    d = evaluate_watchdog(WatchdogState(now(), now() - timedelta(seconds=6), 5, False, False))
    assert not d.healthy and d.kill_switch_required

def test_watchdog_healthy():
    d = evaluate_watchdog(WatchdogState(now(), now() - timedelta(seconds=2), 5, False, False))
    assert d.healthy and not d.kill_switch_required

def test_position_management_is_observational():
    current = PositionSnapshot(now(), PositionState.OPEN, "p1", 1, 2500, "broker")
    observed = PositionSnapshot(now() + timedelta(seconds=1), PositionState.EXIT_PENDING, "p1", 1, 2500, "broker")
    t = transition_position(current, observed)
    assert t.allowed and t.to_state == PositionState.EXIT_PENDING

def test_stale_position_observation_rejected():
    current = PositionSnapshot(now(), PositionState.OPEN, "p1", 1, 2500, "broker")
    observed = PositionSnapshot(now() - timedelta(seconds=1), PositionState.FLAT, "p1", 0, None, "broker")
    assert not transition_position(current, observed).allowed

def test_rollback_requires_explicit_last_known_good():
    r = rollback(RollbackRecord("v2", "v1", False, ""))
    assert r.rollback_allowed and r.last_known_good_version == "v1"

def test_no_implicit_rollback_when_versions_match():
    r = rollback(RollbackRecord("v1", "v1", False, ""))
    assert not r.rollback_allowed
