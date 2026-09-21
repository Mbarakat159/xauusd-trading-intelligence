from evaluation.STAGE5_FROZEN_ABLATION_CASES_V1 import FROZEN_CASES, evaluate_frozen_cases


def test_frozen_case_set_has_required_adversarial_coverage():
    ids = {case.case_id for case in FROZEN_CASES}
    assert ids == {
        "missing-evidence",
        "contradiction",
        "tool-failure-recovery",
        "freshness-boundary",
    }


def test_frozen_ablation_preserves_expected_dispositions():
    results = evaluate_frozen_cases()
    assert all(result.baseline_correct for result in results)
    assert all(result.disciplined_correct for result in results)
    assert all(not result.changed_outcome for result in results)


def test_disciplined_process_improves_contract_score_on_frozen_cases():
    results = evaluate_frozen_cases()
    assert all(result.disciplined_score > result.baseline_score for result in results)


def test_frozen_cases_do_not_hide_causal_boundary_failures():
    results = evaluate_frozen_cases()
    assert all(not any("timestamp" in failure or "stale" in failure for failure in result.failures)
               for result in results)
