# Baseline Protocol V1

## Objective
Make comparisons fair before any performance result is observed.

## Fixed evaluation unit
A decision episode contains:
- one timestamp/cutoff;
- one instrument/feed;
- available observations;
- declared horizon;
- opportunity state;
- hard risk/execution constraints;
- baseline output.

All baselines receive the same information.

## Required baseline outputs
Each baseline must produce:
- action;
- timestamp;
- reason codes;
- required inputs;
- uncertainty/unknowns;
- risk violations;
- model/version identifier.

## Outcome windows
The evaluation framework may record what happened after the decision, but the decision process cannot access it.

For actual trading-quality claims, use forward/shadow observations. Historical cases are for correctness and adversarial testing.

## Primary evaluation dimensions
- reasoning correctness;
- invalidation discipline;
- evidence discipline;
- opportunity identification;
- unnecessary activity;
- risk violations;
- execution feasibility;
- stability by market condition.

No single metric determines promotion.

## Statistical discipline
Before forward evaluation:
- define the sample unit;
- define the primary metrics;
- define the evaluation window;
- define exclusion rules;
- freeze versions;
- define minimum sample requirements.

Do not change these after seeing results.

## WAIT evaluation
WAIT is evaluated on both:
- avoided exposure;
- missed qualified opportunity.

This prevents a system from learning that inactivity is always optimal.
