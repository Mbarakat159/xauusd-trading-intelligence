from datetime import datetime, timedelta, timezone
import pytest

from xauusd_intelligence.shadow import (
    ShadowObservation, ShadowOutcome, attach_outcome, evaluate_shadow,
    freeze_decision, digest_payload,
)

def ts(m=0):
    return datetime(2026, 9, 21, 12, m, tzinfo=timezone.utc)

def obs():
    return ShadowObservation("obs-1", ts(), "XAUUSD", "forward-feed", "demo", digest_payload({"bid": 2500}), "features-v1", "reasoning-v1", "safety-v1")

def test_decision_is_frozen_before_outcome():
    d = freeze_decision(obs(), "dec-1", "WAIT", {"action": "WAIT"}, "WAIT", "safety-digest")
    assert d.frozen_before_outcome

def test_outcome_must_follow_decision():
    d = freeze_decision(obs(), "dec-1", "WAIT", {}, "WAIT", "s")
    with pytest.raises(ValueError):
        attach_outcome(d, ShadowOutcome("dec-1", ts(), "o", "forward-feed"))

def test_outcome_links_to_same_decision():
    d = freeze_decision(obs(), "dec-1", "WAIT", {}, "WAIT", "s")
    o = attach_outcome(d, ShadowOutcome("dec-1", ts(1), "o", "forward-feed"))
    assert o.decision_id == "dec-1"

def test_wrong_outcome_reference_rejected():
    d = freeze_decision(obs(), "dec-1", "WAIT", {}, "WAIT", "s")
    with pytest.raises(ValueError):
        attach_outcome(d, ShadowOutcome("dec-2", ts(1), "o", "forward-feed"))

def test_evaluation_detects_duplicates_and_causality():
    d = freeze_decision(obs(), "dec-1", "WAIT", {}, "BLOCK", "s")
    e = evaluate_shadow((d, d), (ShadowOutcome("dec-1", ts(), "o", "feed"),))
    assert e.duplicate_decisions == 1
    assert e.causality_violations == 1

def test_evaluation_counts_actions_and_blocks():
    d1 = freeze_decision(obs(), "dec-1", "WAIT", {}, "WAIT", "s")
    d2 = freeze_decision(obs(), "dec-2", "BLOCK", {}, "BLOCK", "s")
    e = evaluate_shadow((d1, d2), ())
    assert e.actions == {"WAIT": 1, "BLOCK": 1}
    assert e.safety_blocks == 1
