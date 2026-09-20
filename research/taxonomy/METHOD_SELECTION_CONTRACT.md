# Method Selection Contract V1

## Purpose
Choose analytical families according to the observed problem and available evidence, not according to a permanent favorite strategy.

## Selection sequence
1. Define the decision horizon.
2. Inspect deterministic market state.
3. Identify the question: structure, location, momentum, auction, liquidity, volatility, macro/event, execution, or risk.
4. Retrieve the candidate analytical families relevant to that question.
5. For each candidate, resolve its required inputs against the deterministic feature/data capability contracts.
6. Exclude or narrow methods whose required evidence is unavailable; represent the missing evidence explicitly.
7. Select a small set of complementary methods.
8. Identify correlated/redundant evidence and prevent it from being counted as independent support.
9. Generate competing hypotheses.
10. Specify measurable disconfirming conditions.
11. Stop analysis when additional methods add no discriminative information or exceed the analysis budget.

## Required method metadata
Every retrievable analytical family must expose:
- method_id and version;
- analytical question/domain;
- required knowledge objects;
- required deterministic features/data fields;
- optional inputs;
- weak/invalid conditions;
- known failure modes;
- competing interpretations;
- disconfirmation requirements;
- provenance and claim status;
- evaluation status.

A method is not selected merely because its name matches the current market description.

## Evidence and redundancy
Evidence is valuable when it changes the relative plausibility of competing hypotheses, not because there is a large quantity of evidence. Shared source, transformation or causal driver must be represented so downstream reasoning does not double-count correlated evidence.

## Missing-data behavior
- SUFFICIENT: required evidence is available and valid for the declared claim.
- PARTIAL: only a narrower claim is supportable; the narrowed claim must be explicit.
- UNKNOWN: the required evidence is unavailable or invalid.
No proxy may silently replace a required direct measurement.

## Output contract
The selector returns:
- selected_methods;
- selection_reason;
- required_inputs;
- unavailable_inputs;
- narrowed_claims;
- redundancy_flags;
- hypotheses;
- falsification_tests;
- provenance;
- method_versions.

The output is an analytical selection record, not an entry/exit instruction.

## Anti-patterns
- Indicator majority vote.
- "All timeframes agree" as a requirement.
- Selecting a method because it produced a visually attractive historical example.
- Calling a broker tick-volume proxy true order flow.
- Adding indicators until a narrative becomes convincing.
- Changing the method after seeing the outcome.
- Selecting methods before checking data sufficiency.
- Treating method count as evidence strength.
