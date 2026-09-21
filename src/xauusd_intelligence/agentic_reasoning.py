from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence


VERSION = "agentic-reasoning-v1.0.0"


class AgenticStep(str, Enum):
    UNDERSTAND = "understand"
    EXPLORE = "explore"
    PLAN = "plan"
    ACT = "act"
    VERIFY = "verify"
    ITERATE = "iterate"
    REVIEW = "review"


@dataclass(frozen=True)
class AgenticTrace:
    """Observable agent-process record; it contains no hidden chain-of-thought."""

    steps: tuple[AgenticStep, ...]
    evidence_requests: tuple[str, ...] = ()
    verification_checks: tuple[str, ...] = ()
    contradictions: tuple[str, ...] = ()
    recovery_actions: tuple[str, ...] = ()
    final_disposition: str = ""
    version: str = VERSION


@dataclass(frozen=True)
class AgenticEvaluation:
    complete_loop: bool
    evidence_gathered: bool
    verification_present: bool
    contradictions_preserved: bool
    recovery_present: bool
    disposition_preserved: bool
    failures: tuple[str, ...]
    score: int
    version: str = VERSION


_REQUIRED_LOOP = (
    AgenticStep.UNDERSTAND,
    AgenticStep.EXPLORE,
    AgenticStep.PLAN,
    AgenticStep.ACT,
    AgenticStep.VERIFY,
    AgenticStep.REVIEW,
)


def evaluate_trace(trace: AgenticTrace, *, expected_disposition: str | None = None) -> AgenticEvaluation:
    """Evaluate observable process discipline, not model intelligence or profitability."""
    failures: list[str] = []
    positions = {step: i for i, step in enumerate(trace.steps)}

    complete = all(
        step in positions and (i == 0 or positions[_REQUIRED_LOOP[i - 1]] < positions[step])
        for i, step in enumerate(_REQUIRED_LOOP)
    )
    if not complete:
        failures.append("required agentic loop order is incomplete")

    evidence = bool(trace.evidence_requests)
    if not evidence:
        failures.append("no explicit evidence-gathering request recorded")

    verification = bool(trace.verification_checks)
    if not verification:
        failures.append("no explicit verification check recorded")

    contradictions = bool(trace.contradictions)
    if any(x.strip().lower() == "discarded" for x in trace.contradictions):
        failures.append("contradiction was explicitly discarded")

    recovery = bool(trace.recovery_actions)
    if AgenticStep.ITERATE in trace.steps and not recovery:
        failures.append("iteration is claimed without a recovery/refinement action")

    disposition_ok = expected_disposition is None or trace.final_disposition == expected_disposition
    if not disposition_ok:
        failures.append("final disposition differs from expected case disposition")

    score = sum(
        [
            complete,
            evidence,
            verification,
            contradictions or not trace.contradictions,
            recovery or AgenticStep.ITERATE not in trace.steps,
            disposition_ok,
        ]
    )

    return AgenticEvaluation(
        complete,
        evidence,
        verification,
        contradictions or not trace.contradictions,
        recovery or AgenticStep.ITERATE not in trace.steps,
        disposition_ok,
        tuple(failures),
        score,
    )


@dataclass(frozen=True)
class AblationCase:
    case_id: str
    expected_disposition: str
    baseline: AgenticTrace
    disciplined: AgenticTrace


@dataclass(frozen=True)
class AblationResult:
    case_id: str
    baseline_score: int
    disciplined_score: int
    baseline_correct: bool
    disciplined_correct: bool
    changed_outcome: bool
    failures: tuple[str, ...]


def run_ablation(cases: Sequence[AblationCase]) -> tuple[AblationResult, ...]:
    """Compare process variants without treating the result as trading evidence."""
    results: list[AblationResult] = []
    for case in cases:
        base = evaluate_trace(case.baseline, expected_disposition=case.expected_disposition)
        disc = evaluate_trace(case.disciplined, expected_disposition=case.expected_disposition)
        failures = tuple(f"baseline:{x}" for x in base.failures) + tuple(
            f"disciplined:{x}" for x in disc.failures
        )
        results.append(
            AblationResult(
                case.case_id,
                base.score,
                disc.score,
                base.disposition_preserved,
                disc.disposition_preserved,
                case.baseline.final_disposition != case.disciplined.final_disposition,
                failures,
            )
        )
    return tuple(results)
