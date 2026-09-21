from datetime import datetime, timezone
from xauusd_intelligence.features import Quality, Result
from xauusd_intelligence.reasoning import *

def now():
    return datetime(2026, 9, 21, tzinfo=timezone.utc)

def test_missing_evidence_forces_wait():
    e = Evidence("e1","observation","structure observed",Quality.VALID,"feature-layer",independent_group="structure")
    h = Hypothesis("h1","continuation",supporting_evidence=("e1",),required_evidence=("e2",),disconfirmation=("close back below reference",),invalidation=("structural reference breaks",))
    d = reason(ReasoningInput(now(),"intraday",(e,),(),(h,)))
    assert d.action == Action.WAIT
    assert "e2" in d.missing_evidence

def test_conflict_is_preserved():
    e1 = Evidence("e1","observation","break",Quality.VALID,"feature",supports=("h1",),independent_group="structure")
    e2 = Evidence("e2","observation","rejection",Quality.VALID,"feature",contradicts=("h1",),independent_group="structure")
    h = Hypothesis("h1","continuation",supporting_evidence=("e1",),contradicting_evidence=("e2",),disconfirmation=("rejection persists",))
    d = reason(ReasoningInput(now(),"intraday",(e1,e2),(),(h,)))
    assert d.supporting_evidence == ("e1",)
    assert d.contradicting_evidence == ("e2",)

def test_data_failure_blocks():
    h=Hypothesis("h1","test")
    d=reason(ReasoningInput(now(),"intraday",(),(),(h,),data_quality_ok=False))
    assert d.action == Action.BLOCK

def test_no_hypothesis_waits():
    d=reason(ReasoningInput(now(),"intraday",(),(),()))
    assert d.action == Action.WAIT

def test_future_feature_rejected():
    r=Result("F001",True,Quality.VALID,datetime(2026,9,22,tzinfo=timezone.utc))
    try:
        reason(ReasoningInput(now(),"intraday",(),(),(Hypothesis("h1","x"),),(r,)))
    except ValueError:
        pass
    else:
        assert False

def test_llm_confidence_is_not_probability():
    try:
        reason(ReasoningInput(now(),"intraday",(),(),(Hypothesis("h1","x"),),llm_confidence=0.9))
    except ValueError:
        pass
    else:
        assert False

def test_digest_changes_when_evidence_content_changes():
    e1 = Evidence("e1", "observation", "break above range", Quality.VALID, "feature")
    h = Hypothesis("h1", "continuation", supporting_evidence=("e1",), disconfirmation=("close back inside range",))
    d1 = reason(ReasoningInput(now(), "intraday", (e1,), (), (h,)))
    e2 = Evidence("e1", "observation", "break above range then reject", Quality.VALID, "feature")
    d2 = reason(ReasoningInput(now(), "intraday", (e2,), (), (h,)))
    assert d1.immutable_input_digest != d2.immutable_input_digest

def test_mtf_conflict_is_not_majority_voted():
    high_tf = Evidence("e1", "structure", "higher timeframe bullish", Quality.VALID, "feature", timeframe="1h", independent_group="structure-1h")
    low_tf = Evidence("e2", "structure", "lower timeframe bearish", Quality.VALID, "feature", timeframe="5m", independent_group="structure-5m")
    h = Hypothesis("h1", "continuation", supporting_evidence=("e1",), contradicting_evidence=("e2",), disconfirmation=("5m rejection persists",))
    d = reason(ReasoningInput(now(), "intraday", (high_tf, low_tf), (), (h,)))
    assert d.action == Action.MONITOR
    assert d.supporting_evidence == ("e1",)
    assert d.contradicting_evidence == ("e2",)

def test_unknown_order_flow_does_not_become_support():
    proxy = Evidence("e1", "volume", "broker tick activity proxy", Quality.UNKNOWN, "broker-feed", venue="CFD", timeframe="5m")
    h = Hypothesis("h1", "continuation", supporting_evidence=("e1",), required_evidence=("e1",))
    d = reason(ReasoningInput(now(), "intraday", (proxy,), (), (h,)))
    assert d.action == Action.WAIT
    assert "e1" in d.missing_evidence

def test_correlated_evidence_is_not_counted_as_independent_votes():
    e1 = Evidence("e1", "structure", "break", Quality.VALID, "feature-a", independent_group="same-structure")
    e2 = Evidence("e2", "indicator", "momentum", Quality.VALID, "feature-b", independent_group="same-structure")
    h = Hypothesis("h1", "continuation", supporting_evidence=("e1", "e2"), disconfirmation=("reversal",))
    d = reason(ReasoningInput(now(), "intraday", (e1, e2), (), (h,)))
    assert d.action == Action.MONITOR
    assert d.supporting_evidence == ("e1", "e2")
