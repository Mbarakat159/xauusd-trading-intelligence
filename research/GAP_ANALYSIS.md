# Research Gap Analysis

Status: active.

## Covered well enough for the next research stage

- agentic architecture principles;
- broad trading-methodology taxonomy;
- market-regime dimensions;
- multi-timeframe reasoning;
- evidence/provenance rules;
- risk and execution separation;
- trade-quality dimensions.

## Important gaps still requiring evidence

### 1. Gold-specific microstructure
Need sources addressing XAUUSD/spot gold/futures relationships, liquidity, spreads, session behavior, event response and execution conditions.

### 2. Futures versus CFD/spot representation
The intelligence layer must understand that futures order flow and broker CFD/spot data are not identical. Venue coverage and volume semantics must be explicit.

### 3. Regime detection
Need empirical comparison of rule-based, statistical and machine-learning regime descriptions, with strong attention to distribution shift.

### 4. Order-flow availability
Need a capability map showing what can be inferred from OHLC/tick volume versus true trades, footprint, DOM and Level-2 data.

### 5. Macro transmission
Need a structured causal/context map for rates, USD, inflation, central-bank communication, employment and geopolitical/event shocks without turning macro narratives into deterministic signals.

### 6. Execution model
Need broker-specific research for spread, slippage, requotes, market hours, contract specification and data latency.

### 7. Knowledge evaluation
Need adversarial test cases where the system must reject attractive but unsupported narratives.

### 8. Calibration
Need a future calibration framework separating:
- confidence in interpretation;
- confidence in data quality;
- confidence in regime classification;
- confidence in execution assumptions;
- realized outcome probability, which must be measured separately.

## Completion criterion

The research phase is not complete when many documents exist. It is complete when each major concept has:
- definition;
- observable inputs;
- applicability;
- failure modes;
- evidence quality;
- competing interpretations;
- provenance;
- a proposed evaluation test.
