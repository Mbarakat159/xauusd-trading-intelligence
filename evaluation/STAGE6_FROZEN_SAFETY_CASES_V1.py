from datetime import datetime, timedelta, timezone

from xauusd_intelligence.safety import (
    PositionState, SafetyDisposition, SafetyInput, SafetyLimits, ToolHealth,
    evaluate_safety,
)

FROZEN_CASE_IDS = (
    "healthy-allow",
    "stale-data-wait",
    "spread-block",
    "exposure-block",
    "tool-failure-block",
    "watchdog-block",
)

NOW = datetime(2026, 9, 21, 12, tzinfo=timezone.utc)
LIMITS = SafetyLimits(1.0, 5, 0.5, 100, 80, 3, 10, 5)


def _base(**kwargs):
    values = dict(
        as_of=NOW, upstream_action="TRADE", quote_ts=NOW,
        bid=2500.0, ask=2500.5, expected_price=2500.25,
        requested_exposure=10, current_gross_exposure=20,
        current_net_exposure=10, current_open_positions=1,
        data_age_seconds=2, tool_health=ToolHealth.HEALTHY,
        watchdog_gap_seconds=1, kill_switch_active=False,
        position_state=PositionState.OPEN,
    )
    values.update(kwargs)
    return SafetyInput(**values)


FROZEN_CASES = (
    ("healthy-allow", _base(), SafetyDisposition.ALLOW),
    ("stale-data-wait", _base(data_age_seconds=11), SafetyDisposition.WAIT),
    ("spread-block", _base(ask=2501.1), SafetyDisposition.BLOCK),
    ("exposure-block", _base(current_gross_exposure=95), SafetyDisposition.BLOCK),
    ("tool-failure-block", _base(tool_health=ToolHealth.FAILED), SafetyDisposition.BLOCK),
    ("watchdog-block", _base(watchdog_gap_seconds=6), SafetyDisposition.BLOCK),
)


def evaluate_frozen_cases():
    results = []
    for case_id, inp, expected in FROZEN_CASES:
        actual = evaluate_safety(inp, LIMITS).disposition
        results.append({
            "case_id": case_id,
            "expected": expected.value,
            "actual": actual.value,
            "correct": actual == expected,
        })
    return results
