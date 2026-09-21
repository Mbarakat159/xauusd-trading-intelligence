# Stage 7 — Forward Shadow V1

## Status
STARTED / CONTRACT IMPLEMENTED / FORWARD EVALUATION PENDING

## Purpose
Run the intelligence stack against forward/live XAUUSD observations without sending live orders. This stage measures correctness and stability of the analytical process before any integration or execution.

## Hard boundary
- no broker order submission;
- no live position opening/closing;
- no historical backtest used as proof;
- no outcome information may enter a decision made before that outcome;
- no online modification of strategy, risk limits, features, or knowledge;
- no modification of `autonomous-xauusd-agent`.

## Frozen decision protocol
For every forward observation:
1. assign a unique observation ID and timestamp;
2. record source and venue;
3. record the versions of deterministic features, reasoning, and safety;
4. create the analytical decision;
5. freeze its digest before any future outcome is attached;
6. only later observations may create an outcome record.

The shadow layer enforces the temporal boundary. Outcomes observed at or before the decision timestamp are rejected.

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

## Metrics
The evaluation records:
- total decisions;
- action distribution;
- safety BLOCK count;
- duplicate decision IDs;
- causal/outcome-link violations.

Stage-level evaluation must additionally examine reasoning correctness, feature correctness, regime behavior, method selection, decision quality, WAIT opportunity cost, execution assumptions, stability, and robustness.

## Forward evidence rule
Synthetic tests prove the shadow contract only. Stage 7 cannot be marked PASSED from synthetic tests alone. A real forward/shadow evaluation window with frozen versions is required.

## Current implementation
`src/xauusd_intelligence/shadow.py` provides the immutable observation/decision/outcome records, temporal enforcement, payload digests, and evaluation counters. `src/xauusd_intelligence/forward_capture.py` provides the frozen-window validation boundary. Both are source-agnostic and do not submit orders.

## Gate remains open
Stage 7 cannot be marked PASSED until a real forward/shadow evaluation window has produced observations and later outcomes under frozen versions, followed by the defined evaluation review.
