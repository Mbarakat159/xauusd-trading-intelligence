from datetime import datetime, timezone
import pytest

from xauusd_intelligence.forward_capture import ForwardCapture, ForwardWindow, FrozenVersions
from xauusd_intelligence.shadow import ShadowObservation, ShadowOutcome, digest_payload, freeze_decision

def ts(m=0): return datetime(2026, 9, 21, 12, m, tzinfo=timezone.utc)

def window():
    return ForwardWindow("window-1", "XAUUSD", "forward-feed", "demo", ts(), FrozenVersions("features-v1", "reasoning-v1", "safety-v1"))

def observation(feature_version='features-v1'):
    return ShadowObservation("obs-1", ts(), "XAUUSD", "forward-feed", "demo", digest_payload({"bid": 2500}), feature_version, "reasoning-v1", "safety-v1")

def test_window_enforces_frozen_versions():
    c = ForwardCapture(window()); c.record_observation(observation()); assert c.observation_count == 1

def test_window_rejects_version_change():
    c = ForwardCapture(window())
    with pytest.raises(ValueError, match='feature version'): c.record_observation(observation('features-v2'))

def test_window_rejects_duplicate_observation():
    c = ForwardCapture(window()); c.record_observation(observation())
    with pytest.raises(ValueError, match='duplicate observation'): c.record_observation(observation())

def test_decision_requires_known_observation():
    c = ForwardCapture(window()); o = observation(); c.record_observation(o)
    c.record_decision(freeze_decision(o, 'dec-1', 'WAIT', {'x': 1}, 'WAIT', 's')); assert c.decision_count == 1

def test_outcome_requires_later_timestamp():
    c = ForwardCapture(window()); o = observation(); c.record_observation(o); c.record_decision(freeze_decision(o, 'dec-1', 'WAIT', {}, 'WAIT', 's'))
    with pytest.raises(ValueError): c.record_outcome(ShadowOutcome('dec-1', ts(), 'outcome', 'forward-feed'))

def test_snapshot_contains_only_recorded_items():
    c = ForwardCapture(window()); o = observation(); c.record_observation(o); c.record_decision(freeze_decision(o, 'dec-1', 'WAIT', {}, 'WAIT', 's')); c.record_outcome(ShadowOutcome('dec-1', ts(1), 'outcome', 'forward-feed'))
    observations, decisions, outcomes = c.snapshot(); assert len(observations) == len(decisions) == len(outcomes) == 1