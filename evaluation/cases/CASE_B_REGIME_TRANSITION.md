# Case B — Regime Transition

## Purpose
Test detection of a transition rather than forcing trend/range classification.

## Setup
Price has compressed after a directional move. Volatility and range metrics are changing, but direction is not yet confirmed.

## Expected invariants
- Represent uncertainty/transition explicitly.
- Separate observed compression from predicted breakout direction.
- Do not promote a breakout hypothesis to fact.
- Identify observations that would confirm expansion.

## Acceptable actions
MONITOR or WAIT unless independent evidence establishes a valid opportunity.
