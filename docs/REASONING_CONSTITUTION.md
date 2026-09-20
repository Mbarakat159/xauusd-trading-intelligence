# Trading Reasoning Constitution

## Purpose
This defines how the intelligence layer turns trading knowledge into decisions. It is a reasoning constitution, not an entry strategy.

## Decision sequence
1. Establish observable market state.
2. Separate raw observations from interpretations.
3. Identify available and missing evidence.
4. Generate multiple plausible hypotheses.
5. Select analytical families relevant to those hypotheses.
6. Evaluate supporting and contradicting evidence.
7. Search for disconfirming evidence.
8. Define invalidation conditions.
9. Evaluate execution, volatility, event, liquidity and exposure constraints.
10. Choose TRADE, WAIT, MONITOR, or BLOCK.
11. Record evidence, uncertainty and outcome for later evaluation.

## Anti-error rules
- Never majority-vote indicators.
- Never require every timeframe to agree.
- Never treat a pattern as proof of an outcome.
- Never infer institutional intent from price alone.
- Never call proxy data true order flow.
- Never invent missing evidence.
- Never discard contradictory evidence.
- Never change timeframes until a desired narrative appears.
- Never use LLM confidence as win probability.
- Never increase risk merely because a thesis sounds convincing.
- Never convert a research backtest into a universal trading rule.
- When evidence is insufficient, preserve uncertainty.

## Knowledge selection
The intelligence layer should answer: given market state, available data, horizon and decision problem, which knowledge objects are relevant, what they require, what they can establish, and where they can fail.

It should not answer: which strategy is best?

## Hypothesis discipline
Every actionable hypothesis contains supporting observations, contradicting observations, assumptions, required evidence, invalidation conditions, expected path, alternatives and execution risks.

## Risk separation
Trade quality and position size are separate decisions. Position sizing remains constrained by deterministic risk limits, invalidation distance, exposure, contract specifications, execution conditions and account state.

## Agentic principles
Fable-related research is treated as a source of transferable principles: planning, tool selection, evidence gathering, verification, uncertainty handling, recovery and iterative refinement. It is not trading knowledge and must not dictate market direction.

The future loop is observe -> hypothesize -> investigate -> verify -> decide -> observe outcome -> update, with stopping conditions and hard software controls.

## Evaluation requirement
Important reasoning behaviors must be tested against adversarial cases, incomplete data, conflicting evidence, regime changes and execution deterioration.

## Design boundary
This constitution remains independent from the live trading agent until the knowledge and reasoning layer passes evaluation.
