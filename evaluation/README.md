# Intelligence Evaluation Benchmark

Purpose: test whether the future agent can reason about markets rather than merely recite trading terminology.

## Benchmark families

### A. Regime recognition
Given market observations, identify plausible state dimensions and uncertainty.

### B. MTF reasoning
Given conflicting timeframes, explain the relationship instead of voting between signals.

### C. Method selection
Given a market state, select relevant analytical families and explain why other families are less informative.

### D. Hypothesis competition
Generate at least two plausible explanations for the same movement and identify discriminating evidence.

### E. Invalidation
State what observation would falsify each hypothesis.

### F. Risk construction
Evaluate stop location, volatility, execution quality and exposure without converting subjective confidence directly into position size.

### G. Evidence discipline
Distinguish raw observation, derived measurement, empirical research, framework interpretation and unsupported claims.

### H. Event handling
Recognize pre-event, event and post-event conditions and account for execution uncertainty.

### I. Recovery
When new data contradict an earlier conclusion, update the state and explain what changed.

### J. Memory
Store structured decision state, evidence, outcome and calibration information rather than unbounded transcript history.

## Anti-gaming requirements

A benchmark case should sometimes:
- contain incomplete data;
- contain deliberately conflicting observations;
- contain tempting but unsupported labels;
- change regime after the initial observation;
- include a misleading indicator;
- include execution deterioration;
- require a WAIT or BLOCK outcome.

## Passing principle

A strong result is not the one that predicts direction most confidently. It is the one that:
- uses appropriate evidence;
- preserves uncertainty;
- identifies conflicts;
- defines invalidation;
- chooses tools according to context;
- respects deterministic risk constraints;
- updates correctly when evidence changes.
