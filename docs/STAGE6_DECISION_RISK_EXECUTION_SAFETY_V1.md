# Stage 6 — Decision / Risk / Execution Safety V1

## Status
PASSED / V1 IMPLEMENTED — EVALUATION GATE CLOSED

## Scope
Stage 6 adds a deterministic safety boundary around the analytical disposition. It does not create a trading strategy and does not select direction, entry, target, stop, or position size.

## Required capabilities implemented
- hard risk constraints;
- execution-quality checks;
- gross/net exposure checks;
- deterministic data/tool failure handling;
- fail-closed safety behavior;
- open-position state/transition design based on observed state;
- independent watchdog / kill-switch contract;
- explicit last-known-good rollback contract;
- immutable input digest before outcome visibility.

## Safety contract
evaluate_safety accepts an upstream request and explicit caller-supplied limits. It only checks whether the request is safe to pass the boundary. Limits are not inferred by an LLM and are not learned online.

Hard failures include:
- active kill switch;
- unhealthy required tools;
- missing/stale/invalid quotes;
- spread or expected execution deviation above explicit limits;
- stale data;
- gross/net exposure violations;
- open-position count violation;
- unknown position state;
- watchdog heartbeat gap violation.

The layer is fail-closed: a hard safety violation returns BLOCK.

## Open-position management
Position management is observational in V1. PositionSnapshot records broker-observed state and transition_position validates causal state transitions. It never emits an order.

## Watchdog
The watchdog verifies heartbeat freshness and produces a deterministic kill-switch requirement when the heartbeat is missing/stale or a kill-switch/latch is already active.

## Rollback
Rollback is not automatic model self-modification. A rollback target must be an explicitly recorded last-known-good version. The function only validates rollback eligibility; deployment/activation remains outside this repository.

## Explicit boundaries
- no strategy selection;
- no direction;
- no entry price;
- no TP/SL;
- no position sizing;
- no profitability probability;
- no broker order submission;
- no online self-modification;
- no modification of autonomous-xauusd-agent.

## Frozen evaluation gate
The Stage 6 gate uses six frozen synthetic cases in evaluation/STAGE6_FROZEN_SAFETY_CASES_V1.py: healthy allow, stale-data wait, spread block, exposure block, tool-failure block, and watchdog block. The evaluation checks the exact case set and requires every disposition to match its frozen expectation. These cases test safety-contract behavior only; they are not trading-performance evidence.

## Evaluation boundary
Synthetic tests validate deterministic safety, fail-closed behavior, causal position-state handling, watchdog behavior, rollback eligibility, and explicit WAIT versus BLOCK behavior. They are not trading-performance evidence.


## Gate closure
Repository-level CI passed on commit 2ef03176da6b6b29a365badce684799c028bea07. Stage 2 deterministic validation, Stage 4 Gate, and Stage 5 Agentic Reasoning Validation all completed successfully. The frozen Stage 6 safety cases passed through the repository test suite. This is safety-contract evidence only, not live trading or profitability evidence.
