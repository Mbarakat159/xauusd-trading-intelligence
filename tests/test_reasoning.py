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
