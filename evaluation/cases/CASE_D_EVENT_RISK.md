# Case D — Event Risk

## Purpose
Test separation of pre-event, event-window and post-event states.

## Setup
A high-impact scheduled macro event is approaching. Market conditions are volatile and execution quality is not guaranteed.

## Expected invariants
- Record event distance and known severity.
- Do not use the future event outcome.
- Separate directional thesis from execution/event risk.
- Allow WAIT or reduced activity when evidence is insufficient.

## Forbidden reasoning
“The event will make gold rise, so enter before it.”
