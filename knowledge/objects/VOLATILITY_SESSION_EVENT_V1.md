# Volatility, Session & Event Knowledge Objects V1

## Operationalization dependency
Measurement semantics use `research/features/FEATURE_DEFINITIONS_V1.md`. Window sizes, baselines and calendars are versioned inputs.

## K023 Volatility Expansion / Compression
- type: concept
- definition: A change in realized price variability relative to a causal baseline.
- operational_definition: Compare a fixed volatility measure with a predeclared rolling/reference distribution; if the baseline cannot be constructed causally, return UNKNOWN.
- observable_inputs: returns, TR, ATR, realized volatility.
- data_requirements: causal OHLC with sufficient history for the baseline.
- applicable_conditions: regime and execution assessment.
- weak_conditions: insufficient sample or feed discontinuity.
- failure_modes: mixing event shock with ordinary expansion.
- competing_interpretations: regime transition, scheduled event, data anomaly.
- evidence_refs: FEATURE_DEFINITIONS_V1, REGIME_CONTRACT_V1
- claim_status: CLAIMED
- evaluation_tests: boundary and transition tests.
- decision_safety: descriptive state.

## K024 Session State
- type: concept
- definition: A causal classification of the current market session/context using predefined venue/time rules.
- operational_definition: Map timestamp to explicitly versioned session calendar and timezone; calendar ambiguity yields UNKNOWN.
- observable_inputs: timestamp, venue/session calendar.
- data_requirements: correct timezone/calendar.
- applicable_conditions: intraday analysis.
- weak_conditions: holidays, DST transitions, venue-specific schedules.
- failure_modes: wrong timezone or stale calendar.
- competing_interpretations: session labels describe time, not direction.
- evidence_refs: EVENT_SESSION_MODEL, DATA_QUALITY_CONTRACT, FEATURE_DEFINITIONS_V1
- claim_status: CLAIMED
- evaluation_tests: DST, holiday, boundary tests.
- decision_safety: never treat session as signal.

## K025 Event Risk State
- type: concept
- definition: A state describing proximity to, presence within, or aftermath of a scheduled market event.
- operational_definition: Use versioned event timestamp, timezone, event window and post-event resolution rule; ambiguous event metadata yields UNKNOWN.
- observable_inputs: event calendar, current timestamp, price/volatility.
- data_requirements: timestamped event source.
- applicable_conditions: macro-sensitive analysis and execution.
- weak_conditions: unscheduled events or unreliable calendar.
- failure_modes: future-event leakage, wrong timezone, stale calendar.
- competing_interpretations: pre-event positioning, event shock, post-event repricing.
- evidence_refs: G005, CASE_D_EVENT_RISK, FEATURE_DEFINITIONS_V1
- claim_status: CLAIMED
- evaluation_tests: event-window boundary and missing-calendar tests.
- decision_safety: hard risk context when event data are trusted.
