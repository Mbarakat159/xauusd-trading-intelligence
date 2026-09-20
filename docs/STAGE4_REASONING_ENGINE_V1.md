# Stage 4 — Reasoning Engine V1

## Scope
This stage implements the first reasoning kernel on top of the frozen deterministic observation and knowledge contracts. It is an analytical reasoning layer, not a broker, execution engine, strategy optimizer, or profitability model.

## Fixed flow
OBSERVATIONS -> DATA SUFFICIENCY -> METHOD CONTEXT -> COMPETING HYPOTHESES -> SUPPORT/CONTRADICTION -> DISCONFIRMATION -> INVALIDATION -> REASONING DISPOSITION

Execution authorization remains outside this module.

## Implemented contracts
- timestamp-causal inputs only;
- deterministic feature results can become provenance-preserving evidence;
- explicit missing/invalid evidence;
- multiple hypotheses are represented rather than collapsed;
- supporting and contradicting evidence are preserved;
- correlated evidence is grouped and not counted as independent votes;
- missing required evidence yields WAIT;
- failed data-quality contract yields BLOCK;
- contradiction without an explicit disconfirmation path yields MONITOR;
- no valid support yields WAIT;
- Stage 4 does not produce position size, TP, SL, entry price, or profit probability;
- LLM confidence is explicitly rejected as a probability/execution field;
- immutable decision input digest is recorded before any outcome can be attached.

## Important limitation
This V1 kernel does not yet implement live knowledge retrieval or an LLM planner. Those are subsequent Stage 4 increments and must be evaluated against the existing contracts rather than replacing them.

## Evaluation boundary
Historical/synthetic cases may test causality, leakage, contradiction preservation, missing-data behavior, and reasoning correctness. They are not evidence of live XAUUSD profitability.
