from xauusd_intelligence.agentic_reasoning import (
    AgenticStep,
    AgenticTrace,
    AblationCase,
    evaluate_trace,
    run_ablation,
)


def disciplined(disposition="WAIT"):
    return AgenticTrace(
        steps=(
            AgenticStep.UNDERSTAND,
            AgenticStep.EXPLORE,
            AgenticStep.PLAN,
            AgenticStep.ACT,
            AgenticStep.VERIFY,
            AgenticStep.REVIEW,
        ),
        evidence_requests=("check required evidence",),
        verification_checks=("verify timestamp causality",),
        contradictions=("preserve competing interpretation",),
        final_disposition=disposition,
    )


def test_disciplined_trace_satisfies_agentic_contract():
    result = evaluate_trace(disciplined(), expected_disposition="WAIT")
    assert result.complete_loop
    assert result.evidence_gathered
    assert result.verification_present
    assert result.disposition_preserved
    assert result.causal_boundary_preserved
    assert result.failures == ()


def test_missing_verification_is_detected():
    trace = disciplined()
    trace = AgenticTrace(
        steps=trace.steps,
        evidence_requests=trace.evidence_requests,
        verification_checks=(),
        contradictions=trace.contradictions,
        final_disposition=trace.final_disposition,
    )
    result = evaluate_trace(trace, expected_disposition="WAIT")
    assert not result.verification_present
    assert "no explicit verification check recorded" in result.failures


def test_iterate_requires_recovery_action():
    trace = AgenticTrace(
        steps=disciplined().steps + (AgenticStep.ITERATE,),
        evidence_requests=("check",),
        verification_checks=("verify",),
        final_disposition="WAIT",
    )
    result = evaluate_trace(trace, expected_disposition="WAIT")
    assert not result.recovery_present


def test_ablation_does_not_allow_process_discipline_to_change_case_truth():
    baseline = AgenticTrace(
        steps=(AgenticStep.UNDERSTAND,),
        final_disposition="WAIT",
    )
    result = run_ablation(
        (
            AblationCase(
                "missing-evidence",
                "WAIT",
                baseline,
                disciplined("WAIT"),
            ),
        )
    )[0]
    assert not result.baseline_correct
    assert result.disciplined_correct
    assert not result.changed_outcome


def test_contradiction_is_not_silently_discarded():
    trace = disciplined()
    trace = AgenticTrace(
        steps=trace.steps,
        evidence_requests=trace.evidence_requests,
        verification_checks=trace.verification_checks,
        contradictions=("discarded",),
        final_disposition="WAIT",
    )
    result = evaluate_trace(trace, expected_disposition="WAIT")
    assert not result.contradictions_preserved
    assert "contradiction was explicitly discarded" in result.failures


def test_tool_failure_requires_recovery_when_iterating():
    trace = AgenticTrace(
        steps=disciplined().steps + (AgenticStep.ITERATE,),
        evidence_requests=("tool failed; retry bounded evidence request",),
        verification_checks=("verify retry result",),
        recovery_actions=("retry evidence request once",),
        final_disposition="WAIT",
    )
    result = evaluate_trace(trace, expected_disposition="WAIT")
    assert result.recovery_present
    assert result.failures == ()


def test_wrong_disposition_is_failure_even_with_complete_process():
    result = evaluate_trace(disciplined("MONITOR"), expected_disposition="WAIT")
    assert not result.disposition_preserved
    assert "final disposition differs from expected case disposition" in result.failures


def test_future_evidence_violates_causal_boundary():
    trace = AgenticTrace(
        steps=disciplined().steps,
        evidence_requests=("check required evidence",),
        verification_checks=("verify source timestamp",),
        contradictions=disciplined().contradictions,
        final_disposition="WAIT",
        decision_timestamp="2026-09-21T10:00:00Z",
        evidence_timestamps=("2026-09-21T10:01:00Z",),
    )
    result = evaluate_trace(trace, expected_disposition="WAIT")
    assert not result.causal_boundary_preserved
    assert "evidence timestamp is after decision timestamp" in result.failures


def test_stale_evidence_violates_declared_freshness_boundary():
    trace = AgenticTrace(
        steps=disciplined().steps,
        evidence_requests=("check current evidence",),
        verification_checks=("verify source timestamp",),
        contradictions=disciplined().contradictions,
        final_disposition="WAIT",
        decision_timestamp="2026-09-21T10:00:00Z",
        evidence_timestamps=("2026-09-21T09:00:00Z",),
        max_evidence_age_seconds=1800,
    )
    result = evaluate_trace(trace, expected_disposition="WAIT")
    assert not result.causal_boundary_preserved
    assert "evidence is stale beyond declared freshness boundary" in result.failures


def test_valid_causal_evidence_passes_boundary():
    trace = AgenticTrace(
        steps=disciplined().steps,
        evidence_requests=("check required evidence",),
        verification_checks=("verify source timestamp",),
        contradictions=disciplined().contradictions,
        final_disposition="WAIT",
        decision_timestamp="2026-09-21T10:00:00Z",
        evidence_timestamps=("2026-09-21T09:50:00Z",),
        max_evidence_age_seconds=1800,
    )
    result = evaluate_trace(trace, expected_disposition="WAIT")
    assert result.causal_boundary_preserved
