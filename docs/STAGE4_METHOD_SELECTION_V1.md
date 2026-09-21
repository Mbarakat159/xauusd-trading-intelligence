# Stage 4 — Method Selection / Knowledge Retrieval V1

## Purpose

This increment adds a bounded analytical-family selector and knowledge retrieval contract on top of the Stage 4 reasoning kernel. It does not choose a trading strategy, market direction, entry, exit, target, stop, size, or probability.

## Contract

1. Define the analytical question and decision horizon outside the selector.
2. Inspect available deterministic/data capabilities before selecting a method.
3. Exclude methods whose required inputs are unavailable.
4. Retrieve knowledge by declared analytical domain and required inputs.
5. Preserve missing evidence as unavailable; no proxy is silently substituted.
6. Avoid duplicate analytical families with identical required-input contracts.
7. Preserve provenance, claim status, failure modes and disconfirmation requirements.
8. Stop when the method budget is reached or additional methods add no distinct required-input information.
9. The selector output is an analytical selection record, not an execution instruction.

## Safety boundary

The selector cannot:
- produce an entry price;
- produce TP/SL;
- produce position size;
- produce profit probability;
- authorize a broker action;
- treat method count as evidence strength;
- majority-vote indicators or timeframes.

## Evaluation boundary

Tests cover unavailable inputs, redundant methods, scoped retrieval and the no-evidence case. These tests validate selection mechanics only; they are not profitability evidence.

## Validation

This branch validates repository-level execution of the Stage 4 increment.
