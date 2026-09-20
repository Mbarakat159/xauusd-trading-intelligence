# Feature Test Plan V1

## Goal
Verify deterministic observations before they can influence reasoning.

## Test classes
1. Formula tests: known inputs produce exact expected outputs.
2. Boundary tests: zero range, missing previous close, equal highs/lows, empty windows.
3. Causality tests: changing future observations must not change a feature at an earlier decision timestamp.
4. Confirmation-delay tests: confirmed structures appear only after their confirmation condition.
5. Data-quality tests: stale, missing, invalid and conflicting inputs propagate UNKNOWN/quality flags.
6. Time tests: timezone, DST and session-boundary behavior.
7. Version tests: changing parameters or definitions changes feature version and never silently rewrites old records.

## Feature-specific invariants
- OHLC geometry obeys high >= max(open, close) and low <= min(open, close).
- TR uses only current OHLC and immediately preceding valid close.
- Returns require a valid previous close.
- Realized volatility uses only returns available by the cutoff.
- Range position is UNKNOWN when high == low.
- Confirmed swing timestamps are delayed by the declared confirmation rule.
- Structural distances reference only levels already observable at the cutoff.
- Spread requires same-source bid/ask; it is never reconstructed from OHLC.
- Activity is labeled as tick/activity proxy unless centralized transaction volume is actually supplied.
- Event distance cannot expose event outcomes before publication.

## Required test evidence
Every promoted feature must have:
- deterministic test vectors;
- causality test;
- missing-data test;
- timestamp test;
- parameter/version record;
- known limitations.

No feature passes because its values "look right" on a chart.
