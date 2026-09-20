# Regime Evaluation Specification

## Objective
Test whether a regime representation improves analytical selection without turning regime labels into trading signals.

## Regime representation
Represent market state as probabilities or calibrated scores across independent dimensions:
- directional structure;
- volatility;
- liquidity/activity;
- auction/location;
- event state;
- structural transition.

The system may remain uncertain or mixed. A forced single label is not allowed when evidence is ambiguous.

## Deterministic inputs
Examples include confirmed structure, return distributions, ATR/realized volatility, range compression/expansion, spread/activity, session state and event proximity. Each input must have provenance and a causal timestamp.

## Evaluation tasks
1. State estimation from observations.
2. Transition detection.
3. Calibration of regime probabilities.
4. Stability under small input changes.
5. Detection of missing-data uncertainty.
6. Method-selection usefulness: whether regime information changes which analytical families are appropriate.

## Failure tests
- trend-to-range transition;
- range-to-expansion transition;
- volatility shock;
- event-window distortion;
- conflicting timeframes;
- missing activity/order-flow data;
- broker-feed anomalies.

## Promotion rule
Regime detection is not promoted because its labels look plausible. It must pass deterministic feature tests, calibration checks and adversarial cases, then demonstrate incremental usefulness for method selection or decision quality.
