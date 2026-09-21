from evaluation.STAGE6_FROZEN_SAFETY_CASES_V1 import FROZEN_CASE_IDS, FROZEN_CASES, evaluate_frozen_cases

def test_frozen_case_set_is_exact():
    assert tuple(case_id for case_id, _, _ in FROZEN_CASES) == FROZEN_CASE_IDS

def test_frozen_cases_match_expected_dispositions():
    results = evaluate_frozen_cases()
    assert all(r["correct"] for r in results)
