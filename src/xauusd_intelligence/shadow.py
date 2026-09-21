from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json

VERSION = "forward-shadow-v1.0.0"

class ShadowStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class ShadowObservation:
    observation_id: str
    as_of: datetime
    symbol: str
    source: str
    venue: str | None
    payload_digest: str
    feature_version: str
    reasoning_version: str
    safety_version: str

@dataclass(frozen=True)
class ShadowDecision:
    decision_id: str
    observation_id: str
    as_of: datetime
    action: str
    reasoning_digest: str
    safety_disposition: str
    safety_digest: str
    frozen_before_outcome: bool
    version: str = VERSION

@dataclass(frozen=True)
class ShadowOutcome:
    decision_id: str
    observed_at: datetime
    outcome_digest: str
    source: str

@dataclass(frozen=True)
class ShadowEvaluation:
    total_decisions: int
    actions: dict[str, int]
    safety_blocks: int
    causality_violations: int
    duplicate_decisions: int
    outcome_link_errors: int
    version: str = VERSION

def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("naive timestamp is not allowed")
    return dt.astimezone(timezone.utc)

def digest_payload(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(canonical.encode()).hexdigest()

def freeze_decision(observation: ShadowObservation, decision_id: str, action: str,
                    reasoning_payload: object, safety_disposition: str,
                    safety_digest: str) -> ShadowDecision:
    ts = _utc(observation.as_of)
    digest = digest_payload(reasoning_payload)
    if not decision_id:
        raise ValueError("decision_id is required")
    if not safety_digest:
        raise ValueError("safety digest is required")
    return ShadowDecision(
        decision_id=decision_id,
        observation_id=observation.observation_id,
        as_of=ts,
        action=action,
        reasoning_digest=digest,
        safety_disposition=safety_disposition,
        safety_digest=safety_digest,
        frozen_before_outcome=True,
    )

def attach_outcome(decision: ShadowDecision, outcome: ShadowOutcome) -> ShadowOutcome:
    if outcome.decision_id != decision.decision_id:
        raise ValueError("outcome references a different decision")
    if _utc(outcome.observed_at) <= _utc(decision.as_of):
        raise ValueError("outcome must be observed strictly after the frozen decision")
    return outcome

def evaluate_shadow(decisions: tuple[ShadowDecision, ...],
                    outcomes: tuple[ShadowOutcome, ...]) -> ShadowEvaluation:
    ids = [d.decision_id for d in decisions]
    duplicate = len(ids) - len(set(ids))
    by_id = {d.decision_id: d for d in decisions}
    causality = 0
    linked_errors = 0
    for o in outcomes:
        d = by_id.get(o.decision_id)
        if d is None:
            linked_errors += 1
        elif _utc(o.observed_at) <= _utc(d.as_of):
            causality += 1
    actions: dict[str, int] = {}
    for d in decisions:
        actions[d.action] = actions.get(d.action, 0) + 1
    return ShadowEvaluation(
        total_decisions=len(decisions),
        actions=actions,
        safety_blocks=sum(d.safety_disposition == "BLOCK" for d in decisions),
        causality_violations=causality,
        duplicate_decisions=duplicate,
        outcome_link_errors=linked_errors,
    )
