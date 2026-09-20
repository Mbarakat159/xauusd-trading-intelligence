# Baselines

Baselines answer: what value is added by complexity?

## Required controls
### B0 — WAIT ALWAYS
Never trades. Establishes the opportunity-cost floor and prevents confusing risk avoidance with intelligence.

### B1 — RANDOM CONTROL
A deterministic seeded control with the same opportunity timestamps and hard risk limits. Used only as a sanity control.

### B2 — SIMPLE RULE CONTROL
A deliberately simple, transparent market-state rule set. It must be frozen before comparison.

### B3 — INDICATOR VOTING
A naive correlated-signal baseline. Its purpose is diagnostic, not endorsement.

### B4 — STRUCTURE ONLY
Uses deterministic structure observations without the knowledge/reasoning layer.

### B5 — KNOWLEDGE + REASONING
Uses the reviewed knowledge objects and reasoning constitution, but no autonomous learning updates during the evaluation window.

### B6 — FULL INTELLIGENCE
Adds tested agentic planning/tool selection, evidence search and recovery mechanisms.

## Fair comparison
Every baseline receives the same:
- timestamped market observations;
- available data and missing-data flags;
- decision horizon;
- execution assumptions;
- hard risk constraints;
- opportunity definition.

No baseline may receive future information.

## What must not be compared
Do not compare a sophisticated system using richer future data against a simple system using less information. Do not use win rate alone. Do not rank systems by a single metric.

## Promotion question
For each added layer: what changed, under which conditions, and did it improve a predefined metric without increasing violations or unsupported claims?
