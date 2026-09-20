# Evidence & Robustness Knowledge Objects V1

## K026 Evidence Independence
- type: concept
- definition: The degree to which multiple observations provide non-redundant information about a hypothesis.
- operational_definition: Treat shared source, shared transformation and common causal driver as potential dependence; do not count correlated indicators as independent votes.
- observable_inputs: evidence provenance and relationships.
- data_requirements: source/provenance metadata.
- applicable_conditions: competing-hypothesis evaluation.
- weak_conditions: unknown provenance.
- failure_modes: indicator-counting and double-counting.
- competing_interpretations: two signals may still be complementary despite correlation.
- evidence_refs: EVIDENCE_MODEL, BASELINE_PROTOCOL_V1
- claim_status: CLAIMED
- evaluation_tests: correlated-evidence adversarial cases.
- decision_safety: evidence count never substitutes for discriminative power.

## K027 Disconfirmation Test
- type: method
- definition: A predeclared observable condition that would materially reduce plausibility of a hypothesis.
- operational_definition: Define the hypothesis, expected evidence, disconfirming condition, observation horizon and action if triggered before outcome.
- observable_inputs: hypothesis-specific measurements.
- data_requirements: causal measurements.
- applicable_conditions: all nontrivial hypotheses.
- weak_conditions: hypotheses without measurable consequences.
- failure_modes: vague “wait for confirmation”; post-hoc invalidation.
- competing_interpretations: absence of evidence may be UNKNOWN rather than contradiction.
- evidence_refs: REASONING_CONSTITUTION, CASE_E_DISCONFIRMATION
- claim_status: CLAIMED
- evaluation_tests: disconfirmation case.
- decision_safety: mandatory for material hypotheses.

## K028 Robustness
- type: concept
- definition: Stability of a finding under plausible changes in data quality, parameterization, venue, timing, and reasonable alternative interpretations.
- operational_definition: Declare perturbations before evaluation and compare predefined metrics.
- observable_inputs: evaluation results and provenance.
- data_requirements: versioned test environment.
- applicable_conditions: promotion decisions.
- weak_conditions: tiny sample or unavailable alternative data.
- failure_modes: cherry-picking stable-looking slices.
- competing_interpretations: instability may reflect genuine regime dependence rather than invalidity.
- evidence_refs: PROMOTION_GATES, BASELINE_PROTOCOL_V1
- claim_status: CLAIMED
- evaluation_tests: perturbation, missing-data, regime and venue checks.
- decision_safety: no operational promotion from fragile evidence.
