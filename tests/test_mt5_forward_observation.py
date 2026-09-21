from datetime import datetime, timezone

import pytest

from xauusd_intelligence.forward_capture import ForwardCapture, ForwardWindow, FrozenVersions
from xauusd_intelligence.mt5_forward_observation import build_shadow_observation
from xauusd_intelligence.mt5_market_data import MarketBar, MarketSnapshot, MarketTick


AS_OF = datetime(2026, 9, 21, 19, 2, 46, tzinfo=timezone.utc)
VERSIONS = FrozenVersions("features-v1", "reasoning-v1", "safety-v1")


def make_snapshot() -> MarketSnapshot:
    tick = MarketTick("XAUUSD.sd", 4347.39, 4347.66, AS_OF)
    bars = {
        "M1": (
            MarketBar(
                "XAUUSD.sd",
                "M1",
                datetime(2026, 9, 21, 19, 2, tzinfo=timezone.utc),
                4346.0,
                4348.0,
                4345.5,
                4347.0,
                123,
            ),
        )
    }
    return MarketSnapshot("XAUUSD.sd", tick, bars)


def test_builds_observation_from_snapshot_without_future_fields():
    observation = build_shadow_observation(
        make_snapshot(),
        source="mt5",
        venue="EquitiBrokerageSC-Demo",
        feature_version=VERSIONS.feature_version,
        reasoning_version=VERSIONS.reasoning_version,
        safety_version=VERSIONS.safety_version,
    )

    assert observation.as_of == AS_OF
    assert observation.symbol == "XAUUSD.sd"
    assert observation.source == "mt5"
    assert observation.venue == "EquitiBrokerageSC-Demo"
    assert len(observation.payload_digest) == 64
    assert observation.observation_id.startswith("mt5:XAUUSD.sd:")
    assert "outcome" not in observation.observation_id


def test_same_snapshot_produces_same_identity_and_digest():
    kwargs = {
        "source": "mt5",
        "venue": "EquitiBrokerageSC-Demo",
        "feature_version": VERSIONS.feature_version,
        "reasoning_version": VERSIONS.reasoning_version,
        "safety_version": VERSIONS.safety_version,
    }
    first = build_shadow_observation(make_snapshot(), **kwargs)
    second = build_shadow_observation(make_snapshot(), **kwargs)

    assert first.observation_id == second.observation_id
    assert first.payload_digest == second.payload_digest


def test_snapshot_change_changes_digest_and_identity():
    original = make_snapshot()
    changed_tick = MarketTick("XAUUSD.sd", 4348.39, 4348.66, AS_OF)
    changed = MarketSnapshot("XAUUSD.sd", changed_tick, original.bars)
    kwargs = {
        "source": "mt5",
        "venue": "EquitiBrokerageSC-Demo",
        "feature_version": VERSIONS.feature_version,
        "reasoning_version": VERSIONS.reasoning_version,
        "safety_version": VERSIONS.safety_version,
    }

    first = build_shadow_observation(original, **kwargs)
    second = build_shadow_observation(changed, **kwargs)

    assert first.payload_digest != second.payload_digest
    assert first.observation_id != second.observation_id


def test_observation_enters_forward_capture_with_frozen_versions():
    observation = build_shadow_observation(
        make_snapshot(),
        source="mt5",
        venue="EquitiBrokerageSC-Demo",
        feature_version=VERSIONS.feature_version,
        reasoning_version=VERSIONS.reasoning_version,
        safety_version=VERSIONS.safety_version,
    )
    window = ForwardWindow(
        window_id="window-1",
        symbol="XAUUSD.sd",
        source="mt5",
        venue="EquitiBrokerageSC-Demo",
        started_at=AS_OF,
        versions=VERSIONS,
    )
    capture = ForwardCapture(window)

    capture.record_observation(observation)

    assert capture.observation_count == 1
    assert capture.decision_count == 0
    assert capture.outcome_count == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source", ""),
        ("feature_version", ""),
        ("reasoning_version", ""),
        ("safety_version", ""),
    ],
)
def test_required_frozen_metadata_is_rejected(field, value):
    kwargs = {
        "source": "mt5",
        "venue": "EquitiBrokerageSC-Demo",
        "feature_version": VERSIONS.feature_version,
        "reasoning_version": VERSIONS.reasoning_version,
        "safety_version": VERSIONS.safety_version,
    }
    kwargs[field] = value

    with pytest.raises(ValueError):
        build_shadow_observation(make_snapshot(), **kwargs)


def test_tick_symbol_mismatch_is_rejected():
    snapshot = make_snapshot()
    bad_tick = MarketTick("OTHER", snapshot.tick.bid, snapshot.tick.ask, snapshot.tick.time)
    bad_snapshot = MarketSnapshot(snapshot.symbol, bad_tick, snapshot.bars)

    with pytest.raises(ValueError, match="tick symbol"):
        build_shadow_observation(
            bad_snapshot,
            source="mt5",
            venue="EquitiBrokerageSC-Demo",
            feature_version=VERSIONS.feature_version,
            reasoning_version=VERSIONS.reasoning_version,
            safety_version=VERSIONS.safety_version,
        )
