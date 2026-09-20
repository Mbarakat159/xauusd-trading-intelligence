# Evaluation Architecture

## Purpose
Evaluate whether the intelligence layer improves decision quality without claiming that historical tests prove live profitability.

## Separation of claims
- Reasoning correctness: can the system identify observations, conflicts, missing data, hypotheses, invalidation and appropriate action?
- Feature correctness: are deterministic E0/E1 measurements computed without look-ahead or ambiguous definitions?
- Decision quality: does the system improve forward decision outcomes relative to baselines?
- Trading edge: a separate claim requiring forward evidence and realistic execution costs.

## Evaluation layers
1. Synthetic/adversarial cases: test invariants, contradiction handling and failure recovery.
2. Deterministic feature tests: verify calculations and timestamp causality.
3. Component evaluation: regime, method selection, invalidation, risk construction.
4. Baseline comparison: same information, same decision horizon.
5. Forward shadow mode: live observations and decisions, no live orders.
6. Promotion gate: no integration with the autonomous agent until gates pass.

## Mandatory anti-leakage rules
- Decisions are timestamped before outcomes are known.
- No future bars, future event revisions or future-derived labels are available to the decision process.
- Data provenance includes venue/feed, timestamp, timeframe and freshness.
- Historical/replay cases are used for correctness testing, not as proof of profitability.
- Forward evidence is kept separate from research evidence.

## Core metrics
- Observation accuracy against deterministic ground truth.
- Regime calibration and confusion by regime dimension.
- Hypothesis coverage and contradiction detection.
- Invalidation correctness.
- WAIT/BLOCK precision and opportunity-cost measures.
- Risk/execution constraint violations.
- Baseline deltas with confidence intervals where sample size permits.
- Stability across sessions, volatility states and event proximity.

## Promotion principle
A more complex layer is promoted only when its incremental value is measurable, reproducible and not purchased by violating risk or evidence constraints.
