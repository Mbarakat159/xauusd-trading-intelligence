# Stage 7 — Forward Shadow V1

## Status
STARTED / CONTRACT IMPLEMENTED / FORWARD EVALUATION PENDING

## Frozen forward capture boundary
`src/xauusd_intelligence/forward_capture.py` adds a frozen forward-window session around the existing shadow contract.

The session:
- freezes feature/reasoning/safety versions for the window;
- rejects observations from another source, venue, symbol, or version;
- rejects duplicate observation/decision/outcome identifiers;
- requires decisions to reference recorded observations;
- requires the decision timestamp to equal the observation timestamp;
- requires outcomes to arrive strictly after the frozen decision;
- does not fetch market data, submit orders, or create outcomes.

## Forward feed boundary
The capture layer is source-agnostic. A real feed adapter must supply forward XAUUSD observations from an authorized live/forward source. The repository does not invent or synthesize those observations.

## Gate remains open
Stage 7 cannot be marked PASSED until a real forward/shadow evaluation window has produced observations and later outcomes under frozen versions, followed by the defined evaluation review.