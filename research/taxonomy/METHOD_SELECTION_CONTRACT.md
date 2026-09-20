# Method Selection Contract

## Purpose
Choose analytical families according to the observed problem and available evidence, not according to a permanent favorite strategy.

## Selection sequence
1. Define the decision horizon.
2. Inspect deterministic market state.
3. Identify the question: structure, location, momentum, auction, liquidity, volatility, macro/event, execution, or risk.
4. Check which observations required by each method actually exist.
5. Select a small set of complementary methods.
6. Identify correlated/redundant evidence.
7. Generate competing hypotheses.
8. Specify disconfirming conditions.
9. Stop analysis when additional methods add no discriminative information or exceed the analysis budget.

## Anti-patterns
- Indicator majority vote.
- "All timeframes agree" as a requirement.
- Selecting a method because it produced a visually attractive historical example.
- Calling a broker tick-volume proxy true order flow.
- Adding indicators until a narrative becomes convincing.
- Changing the method after seeing the outcome.

## Evidence utility
Evidence is valuable when it changes the relative plausibility of competing hypotheses, not because there is a large quantity of evidence.

## Output
selected_methods, reason, required_inputs, unavailable_inputs, redundancy_flags, hypotheses and falsification_tests.
