# Evaluation Case Schema

Cases test reasoning safely without pretending that a case library proves trading profitability.

## Required
- case_id
- case_type
- market_context
- data_snapshot
- data_cutoff
- available_timeframes
- available_data_types
- missing_data
- observations_ground_truth
- known_conflicts
- allowed_tools
- expected_invariants
- acceptable_actions
- forbidden_reasoning
- scoring_dimensions
- provenance

## Case types
- MTF conflict
- regime transition
- incomplete data
- contradictory evidence
- misleading indicator
- liquidity/order-flow proxy confusion
- event risk
- execution deterioration
- invalidation ambiguity
- WAIT/BLOCK temptation
- tool failure/recovery
- knowledge contradiction

## Scoring
Cases score dimensions independently:
1. observation fidelity;
2. evidence/provenance discipline;
3. hypothesis diversity;
4. contradiction handling;
5. falsification quality;
6. invalidation quality;
7. risk/execution discipline;
8. action appropriateness;
9. uncertainty calibration;
10. recovery behavior.

A case must never be scored by whether the model guessed the next price direction alone.
