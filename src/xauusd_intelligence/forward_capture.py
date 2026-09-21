from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .shadow import ShadowDecision, ShadowObservation, ShadowOutcome, attach_outcome

VERSION = "forward-capture-v1.0.0"

def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("naive timestamp is not allowed")
    return dt.astimezone(timezone.utc)

@dataclass(frozen=True)
class FrozenVersions:
    feature_version: str
    reasoning_version: str
    safety_version: str

@dataclass(frozen=True)
class ForwardWindow:
    window_id: str
    symbol: str
    source: str
    venue: str | None
    started_at: datetime
    versions: FrozenVersions
    status: str = "OPEN"

class ForwardCapture:
    """Append-only in-memory forward-shadow session."""
    def __init__(self, window: ForwardWindow) -> None:
        if not window.window_id or not window.symbol or not window.source:
            raise ValueError("window_id, symbol, and source are required")
        _utc(window.started_at)
        self.window = window
        self._observations: dict[str, ShadowObservation] = {}
        self._decisions: dict[str, ShadowDecision] = {}
        self._outcomes: dict[str, ShadowOutcome] = {}

    def record_observation(self, observation: ShadowObservation) -> None:
        if observation.symbol != self.window.symbol:
            raise ValueError("observation symbol does not match window")
        if observation.source != self.window.source:
            raise ValueError("observation source does not match window")
        if observation.venue != self.window.venue:
            raise ValueError("observation venue does not match window")
        versions = self.window.versions
        if observation.feature_version != versions.feature_version:
            raise ValueError("feature version differs from frozen window")
        if observation.reasoning_version != versions.reasoning_version:
            raise ValueError("reasoning version differs from frozen window")
        if observation.safety_version != versions.safety_version:
            raise ValueError("safety version differs from frozen window")
        if _utc(observation.as_of) < _utc(self.window.started_at):
            raise ValueError("observation predates forward window")
        if observation.observation_id in self._observations:
            raise ValueError("duplicate observation_id")
        self._observations[observation.observation_id] = observation

    def record_decision(self, decision: ShadowDecision) -> None:
        if not decision.frozen_before_outcome:
            raise ValueError("decision must be frozen before outcome")
        if decision.observation_id not in self._observations:
            raise ValueError("decision references unknown observation")
        if decision.decision_id in self._decisions:
            raise ValueError("duplicate decision_id")
        observation = self._observations[decision.observation_id]
        if _utc(decision.as_of) != _utc(observation.as_of):
            raise ValueError("decision timestamp must match observation timestamp")
        self._decisions[decision.decision_id] = decision

    def record_outcome(self, outcome: ShadowOutcome) -> None:
        if outcome.decision_id not in self._decisions:
            raise ValueError("outcome references unknown decision")
        if outcome.decision_id in self._outcomes:
            raise ValueError("duplicate outcome for decision")
        attach_outcome(self._decisions[outcome.decision_id], outcome)
        self._outcomes[outcome.decision_id] = outcome

    @property
    def observation_count(self) -> int:
        return len(self._observations)

    @property
    def decision_count(self) -> int:
        return len(self._decisions)

    @property
    def outcome_count(self) -> int:
        return len(self._outcomes)

    def snapshot(self):
        return (tuple(self._observations.values()), tuple(self._decisions.values()), tuple(self._outcomes.values()))