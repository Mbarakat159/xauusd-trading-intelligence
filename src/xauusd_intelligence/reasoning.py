from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable, Mapping, Sequence

from .features import Quality, Result

VERSION = "reasoning-engine-v1.0.0"


class Action(str, Enum):
    TRADE = "TRADE"
    WAIT = "WAIT"
    MONITOR = "MONITOR"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    kind: str
    statement: str
    quality: Quality
    source: str
    venue: str | None = None
    timeframe: str | None = None
    feature_ids: tuple[str, ...] = ()
    supports: tuple[str, ...] = ()
    contradicts: tuple[str, ...] = ()
    independent_group: str | None = None


@dataclass(frozen=True)
class MethodCandidate:
    method_id: str
    version: str
    domain: str
    required_inputs: tuple[str, ...] = ()
    unavailable_inputs: tuple[str, ...] = ()
    weak_conditions: tuple[str, ...] = ()
    failure_modes: tuple[str, ...] = ()
    competing_interpretations: tuple[str, ...] = ()
    claim_status: str = "claimed"


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    statement: str
    supporting_evidence: tuple[str, ...] = ()
    contradicting_evidence: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    required_evidence: tuple[str, ...] = ()
    disconfirmation: tuple[str, ...] = ()
    invalidation: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    execution_risks: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReasoningInput:
    as_of: datetime
    horizon: str
    observations: tuple[Evidence, ...]
    methods: tuple[MethodCandidate, ...]
    hypotheses: tuple[Hypothesis, ...]
    deterministic_features: tuple[Result, ...] = ()
    data_quality_ok: bool = True
    llm_confidence: float | None = None


@dataclass(frozen=True)
class ReasoningDecision:
    as_of: datetime
    version: str
    action: Action
    selected_methods: tuple[str, ...]
    hypothesis_ids: tuple[str, ...]
    supporting_evidence: tuple[str, ...]
    contradicting_evidence: tuple[str, ...]
    missing_evidence: tuple[str, ...]
    disconfirmation_tests: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    assumptions: tuple[str, ...]
    reasons: tuple[str, ...]
    immutable_input_digest: str


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("naive timestamp is not allowed")
    return dt.astimezone(timezone.utc)


def _validate(inp: ReasoningInput) -> None:
    _utc(inp.as_of)
    if not inp.horizon:
        raise ValueError("decision horizon is required")
    ids = [e.evidence_id for e in inp.observations]
    if len(ids) != len(set(ids)):
        raise ValueError("evidence IDs must be unique")
    hids = [h.hypothesis_id for h in inp.hypotheses]
    if len(hids) != len(set(hids)):
        raise ValueError("hypothesis IDs must be unique")
    mids = [m.method_id for m in inp.methods]
    if len(mids) != len(set(mids)):
        raise ValueError("method IDs must be unique")
    if inp.llm_confidence is not None:
        raise ValueError("LLM confidence is not an execution or probability field")
    for r in inp.deterministic_features:
        if _utc(r.as_of) > _utc(inp.as_of):
            raise ValueError("future feature result is not allowed")


def _digest(inp: ReasoningInput) -> str:
    # Stable representation of all decision inputs, excluding any outcome fields.
    import hashlib
    import json
    from dataclasses import asdict

    payload = {
        "as_of": _utc(inp.as_of).isoformat(),
        "horizon": inp.horizon,
        "observations": [asdict(e) for e in inp.observations],
        "methods": [asdict(m) for m in inp.methods],
        "hypotheses": [asdict(h) for h in inp.hypotheses],
        "deterministic_features": [asdict(r) for r in inp.deterministic_features],
        "data_quality_ok": inp.data_quality_ok,
    }

    def encode(value):
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, datetime):
            return _utc(value).isoformat()
        raise TypeError(f"unsupported digest value: {type(value)!r}")

    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=encode)
    return hashlib.sha256(canonical.encode()).hexdigest()


def reason(inp: ReasoningInput) -> ReasoningDecision:
    """Run the Stage-4 reasoning kernel.

    This is a reasoning contract implementation, not an execution strategy.
    It deliberately does not assign probabilities, position sizes, entry prices,
    stop/target values, or brokerage actions.
    """
    _validate(inp)

    evidence = {e.evidence_id: e for e in inp.observations}
    methods = {m.method_id: m for m in inp.methods}
    missing: set[str] = set()
    support: list[str] = []
    contradict: list[str] = []
    disconfirm: list[str] = []
    invalidation: list[str] = []
    assumptions: list[str] = []
    reasons: list[str] = []

    if not inp.data_quality_ok:
        return ReasoningDecision(
            _utc(inp.as_of), VERSION, Action.BLOCK, tuple(methods), tuple(h.hypothesis_id for h in inp.hypotheses),
            (), (), ("data_quality",), (), (), (), ("data quality contract not satisfied",), _digest(inp)
        )

    if not inp.hypotheses:
        return ReasoningDecision(
            _utc(inp.as_of), VERSION, Action.WAIT, tuple(methods), (), (), (),
            ("competing hypotheses",), (), (), (), ("no hypotheses supplied",), _digest(inp)
        )

    for h in inp.hypotheses:
        for eid in h.supporting_evidence:
            if eid in evidence and evidence[eid].quality == Quality.VALID:
                support.append(eid)
            else:
                missing.add(eid)
        for eid in h.contradicting_evidence:
            if eid in evidence and evidence[eid].quality == Quality.VALID:
                contradict.append(eid)
            else:
                missing.add(eid)
        for req in h.required_evidence:
            if req not in evidence or evidence[req].quality != Quality.VALID:
                missing.add(req)
        disconfirm.extend(h.disconfirmation)
        invalidation.extend(h.invalidation)
        assumptions.extend(h.assumptions)

    unavailable_methods = [m.method_id for m in inp.methods if m.unavailable_inputs]
    if unavailable_methods:
        reasons.append("one or more selected methods have unavailable required inputs")
        missing.update(f"method:{x}" for x in unavailable_methods)

    # Correlated evidence is not counted repeatedly as independent support.
    groups = {}
    for eid in support:
        group = evidence[eid].independent_group or eid
        groups.setdefault(group, []).append(eid)
    independent_support = list(groups)

    if missing:
        action = Action.WAIT
        reasons.append("required evidence is missing or invalid")
    elif contradict and not disconfirm:
        action = Action.MONITOR
        reasons.append("material contradiction exists without an explicit disconfirmation path")
    elif not independent_support:
        action = Action.WAIT
        reasons.append("no valid supporting evidence")
    else:
        # Stage 4 can formulate a reasoning disposition, but cannot authorize execution.
        action = Action.MONITOR
        reasons.append("reasoning supports a hypothesis; execution authorization remains outside Stage 4")

    return ReasoningDecision(
        _utc(inp.as_of), VERSION, action,
        tuple(methods), tuple(h.hypothesis_id for h in inp.hypotheses),
        tuple(dict.fromkeys(support)), tuple(dict.fromkeys(contradict)),
        tuple(sorted(missing)), tuple(dict.fromkeys(disconfirm)),
        tuple(dict.fromkeys(invalidation)), tuple(dict.fromkeys(assumptions)),
        tuple(reasons), _digest(inp)
    )


def result_as_observation(result: Result, statement: str, source: str, *,
                          evidence_id: str, venue: str | None = None,
                          timeframe: str | None = None) -> Evidence:
    """Convert a deterministic feature result into provenance-preserving evidence."""
    return Evidence(
        evidence_id=evidence_id,
        kind="deterministic_feature",
        statement=statement,
        quality=result.quality,
        source=source,
        venue=venue,
        timeframe=timeframe,
        feature_ids=(result.feature,),
    )
