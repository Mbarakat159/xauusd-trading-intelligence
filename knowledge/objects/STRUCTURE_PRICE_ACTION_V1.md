# Structure & Price Action Knowledge Objects V1

These objects define analytical concepts; they are not entry rules or profitability claims.

## K013 Swing Structure
- type: concept
- definition: A sequence of confirmed swing highs/lows used to describe directional structure.
- operational_definition: A swing is confirmed only after the configured confirmation condition occurs; the confirmation timestamp is the earliest usable timestamp.
- observable_inputs: OHLC, timeframe, swing parameters.
- data_requirements: causally ordered OHLC.
- applicable_conditions: all structural analysis.
- weak_conditions: sparse/incomplete candles, unstable parameters, unresolved transition.
- failure_modes: look-ahead, unconfirmed pivots treated as known, timeframe cherry-picking.
- competing_interpretations: local swing sequence may represent noise rather than durable structure.
- evidence_refs: FEATURE_DEFINITIONS_V1, FEATURE_TEST_PLAN
- claim_status: CLAIMED
- evaluation_tests: causality, delayed confirmation, missing-data cases.
- decision_safety: descriptive only.

## K014 Higher High / Higher Low Sequence
- type: concept
- definition: A directional structural sequence in which confirmed swing relationships are ordered consistently.
- operational_definition: Compare only confirmed swings available at decision time; do not infer future continuation.
- observable_inputs: confirmed swing highs/lows.
- data_requirements: valid OHLC and causal swing confirmation.
- applicable_conditions: directional-structure assessment.
- weak_conditions: transition, compressed ranges, insufficient confirmed swings.
- failure_modes: premature pivot use, ignoring scale/timeframe.
- competing_interpretations: apparent sequence can coexist with weakening momentum or imminent transition.
- evidence_refs: K013, REGIME_CONTRACT_V1
- claim_status: CLAIMED
- evaluation_tests: MTF conflict, regime transition.
- decision_safety: context evidence, never standalone trade proof.

## K015 Break of Structure
- type: concept
- definition: A causal breach of a previously defined structural reference.
- operational_definition: The reference level and break criterion must be defined before the observation; the break timestamp is when the criterion first becomes true.
- observable_inputs: confirmed structural level, OHLC/quote data.
- data_requirements: causal price data.
- applicable_conditions: structural transition analysis.
- weak_conditions: spread expansion, event windows, thin liquidity, ambiguous levels.
- failure_modes: hindsight-selected levels, wick/body ambiguity, false break classification.
- competing_interpretations: continuation, liquidity test, rejection, or structural transition.
- evidence_refs: FEATURE_DEFINITIONS_V1, CASE_A_MTF_CONFLICT
- claim_status: CLAIMED
- evaluation_tests: causality, event-risk, disconfirmation.
- decision_safety: requires confirmation context and invalidation.

## K016 Sweep / Liquidity Test
- type: concept
- definition: A price excursion through a pre-existing reference followed by behavior that may indicate rejection or acceptance.
- operational_definition: The reference, excursion threshold, observation window, and post-excursion classification must be specified before evaluation.
- observable_inputs: price/quote path, structural references, spread if available.
- data_requirements: sufficiently granular causal data.
- applicable_conditions: liquidity/auction hypothesis testing.
- weak_conditions: coarse bars, missing quotes, event shocks.
- failure_modes: labeling every wick as a sweep; post-outcome naming; venue ambiguity.
- competing_interpretations: stop execution, ordinary volatility, breakout acceptance, rejection.
- evidence_refs: CASE_E_DISCONFIRMATION, GOLD_MICROSTRUCTURE
- claim_status: CLAIMED
- evaluation_tests: exact operational labeling and adversarial false-positive cases.
- decision_safety: hypothesis generator, not evidence of institutional intent.

## K017 Acceptance / Rejection
- type: concept
- definition: Observable persistence near/beyond a reference versus movement away from it after interaction.
- operational_definition: Predefine location, observation horizon, persistence/return criteria, and minimum data quality.
- observable_inputs: price path, structural levels, volume/activity where available.
- data_requirements: causal sequence and valid timestamps.
- applicable_conditions: auction and structural analysis.
- weak_conditions: unresolved event windows, sparse data.
- failure_modes: judging acceptance only after later price outcome.
- competing_interpretations: temporary pause, absorption, breakout, failed breakout.
- evidence_refs: K015, K016, REGIME_CONTRACT_V1
- claim_status: CLAIMED
- evaluation_tests: breakout/rejection adversarial cases.
- decision_safety: descriptive classification.

## K018 Displacement
- type: concept
- definition: A relatively large directional price movement compared with a defined local volatility baseline.
- operational_definition: Use a fixed causal baseline and threshold; never select the threshold after seeing the outcome.
- observable_inputs: returns/range/ATR.
- data_requirements: sufficient causal OHLC.
- applicable_conditions: expansion and structural-event detection.
- weak_conditions: event shocks and feed anomalies unless explicitly separated.
- failure_modes: volatility-regime confusion, threshold drift.
- competing_interpretations: genuine repricing, event shock, liquidity vacuum.
- evidence_refs: FEATURE_DEFINITIONS_V1
- claim_status: CLAIMED
- evaluation_tests: threshold invariants, event-risk separation.
- decision_safety: observation only.
