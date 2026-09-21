"""Frozen Stage 5 ablation cases.

Cases are synthetic reasoning-contract fixtures, not market-performance evidence.
Both process variants receive the same observable information boundary.
"""
from xauusd_intelligence.agentic_reasoning import AgenticStep, AgenticTrace, AblationCase, run_ablation


DECISION = "2026-09-21T10:00:00Z"
RECENT = "2026-09-21T09:50:00Z"


def disciplined(disposition: str, *, contradiction: str = "preserve competing interpretation", recovery=()):
    return AgenticTrace(
        steps=(
            AgenticStep.UNDERSTAND,
            AgenticStep.EXPLORE,
            AgenticStep.PLAN,
            AgenticStep.ACT,
            AgenticStep.VERIFY,
            AgenticStep.REVIEW,
        ) + ((AgenticStep.ITERATE,) if recovery else ()),
        evidence_requests=("retrieve required evidence",),
        verification_checks=("verify evidence provenance and disposition",),
        contradictions=(contradiction,),
        recovery_actions=tuple(recovery),
        final_disposition=disposition,
        decision_timestamp=DECISION,
        evidence_timestamps=(RECENT,),
        max_evidence_age_seconds=1800,
    )


def baseline(disposition: str):
    return AgenticTrace(
        steps=(AgenticStep.UNDERSTAND, AgenticStep.EXPLORE, AgenticStep.ACT),
        evidence_requests=("retrieve required evidence",),
        final_disposition=disposition,
        decision_timestamp=DECISION,
        evidence_timestamps=(RECENT,),
        max_evidence_age_seconds=1800,
    )


FROZEN_CASES = (
    AblationCase("missing-evidence", "WAIT", baseline("WAIT"), disciplined("WAIT")),
    AblationCase("contradiction", "MONITOR", baseline("MONITOR"), disciplined("MONITOR")),
    AblationCase(
        "tool-failure-recovery",
        "WAIT",
        baseline("WAIT"),
        disciplined("WAIT", recovery=("retry failed evidence request once",)),
    ),
    AblationCase(
        "freshness-boundary",
        "WAIT",
        baseline("WAIT"),
        disciplined("WAIT"),
    ),
)


def evaluate_frozen_cases():
    return run_ablation(FROZEN_CASES)
