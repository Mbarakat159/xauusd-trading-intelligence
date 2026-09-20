# Decision Log Schema

The log is the primary anti-hindsight record.

## Required fields
- decision_id
- timestamp
- data_cutoff_timestamp
- instrument
- venue_or_feed
- timeframes_observed
- data_quality
- raw_observations
- derived_observations
- regime_state
- available_evidence
- missing_evidence
- candidate_hypotheses
- supporting_evidence
- contradicting_evidence
- disconfirming_tests
- invalidation_conditions
- execution_state
- risk_constraints
- action = TRADE | WAIT | MONITOR | BLOCK
- reason_codes
- knowledge_refs
- baseline_id
- model_version
- knowledge_version
- tool_calls
- uncertainty
- outcome_recorded_at
- outcome

## Immutable-before-outcome rule
All decision fields through outcome must be frozen before outcome data becomes visible to the decision process. Corrections create a new version and retain the original.

## Outcome separation
Outcome records must distinguish:
- thesis failure;
- invalidation/market-structure failure;
- execution failure;
- data failure;
- risk-control intervention;
- no-opportunity / WAIT outcome.

## Calibration
Any confidence-like field is descriptive uncertainty, not win probability, unless separately calibrated and validated.
