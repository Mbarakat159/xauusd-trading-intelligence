# Risk and Execution Intelligence Model

Risk is a separate control layer from market interpretation.

## Trade-quality dimensions

The future intelligence layer may assess:
- market-regime compatibility;
- structural clarity;
- location quality;
- trigger quality;
- invalidation clarity;
- stop efficiency;
- expected path/reward relative to risk;
- volatility compatibility;
- event risk;
- liquidity/execution conditions;
- spread/slippage;
- thesis fragility;
- conflicting evidence;
- exposure and correlation.

## Hard controls

Deterministic software must enforce:
- maximum risk per position;
- maximum aggregate exposure;
- maximum drawdown/stop conditions;
- margin/leverage limits;
- allowed instruments;
- execution sanity checks;
- stale/missing data checks;
- broker/platform state reconciliation.

An LLM should recommend within these constraints, never override them.

## Stop analysis

A stop is not good merely because it is small.

The engine should ask:
- what market observation invalidates the thesis?
- is the stop beyond that invalidation?
- does current volatility make the distance realistic?
- is expected execution quality compatible?
- would a tighter stop merely convert normal noise into a loss?
- would a wider stop destroy risk efficiency?

## Position sizing

Conceptually:

size = allowed risk budget / effective stop distance

Effective stop distance should account for:
- spread;
- expected slippage;
- volatility;
- execution uncertainty;
- instrument contract specifications.

A setup assessment can affect whether a trade is allowed, but subjective confidence should not directly become lot size.

## Action classes

The research layer should eventually support:
- BLOCK
- WAIT
- MONITOR
- ALLOW_WITH_STANDARD_RISK
- ALLOW_WITH_REDUCED_RISK

Exact thresholds belong to later implementation/evaluation, not this research phase.

## Post-trade learning

Store:
- thesis;
- evidence used;
- regime;
- intended invalidation;
- actual execution;
- slippage;
- outcome;
- whether thesis failed or execution failed;
- whether evidence was missing;
- whether reasoning was internally consistent.

Do not label every losing trade as a bad decision.
