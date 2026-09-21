# Stage 5 — Fable / Agentic Reasoning Layer V1

Status: IMPLEMENTED / EVALUATION GATE IN PROGRESS

## Scope

This stage imports agent-process principles, not trading rules. The implementation is model-agnostic and records only observable behavior. It does not copy a hidden or leaked prompt and does not infer a trading strategy from Fable.

Initial principles:

1. Understand the task and scope before acting.
2. Explore and gather the evidence needed for the task.
3. Plan the next verifiable actions.
4. Act through bounded tools/actions.
5. Verify the result against observable evidence.
6. Iterate only when verification exposes an unresolved problem.
7. Review the final result and preserve relevant contradictions.

Public Claude/Fable documentation describes behavioral patterns around tool calls, task completion, verification-oriented workflows and related agentic behavior. These principles are treated as hypotheses to evaluate, not as proven improvements. See the cited public documentation and agent-evaluation literature. [Source: Anthropic Fable 5.1 prompting documentation; source URL recorded in project research log.] 

## Trading-intelligence boundary

The Stage 5 layer MUST NOT:

- select a trading direction;
- create an entry, target, stop or position size;
- convert LLM confidence into probability;
- majority-vote indicators or timeframes;
- override deterministic data-quality or risk constraints;
- use Fable behavior as evidence that a trading method works;
- modify the master plan or the separate autonomous agent.

It operates above the Stage 4 reasoning contracts and below any future deterministic decision/risk layer.

## Observable contract

AgenticTrace records only externally inspectable process facts:

- ordered agentic steps;
- evidence requests;
- verification checks;
- preserved contradictions;
- recovery/refinement actions;
- final disposition;
- decision timestamp and evidence timestamps;
- an optional declared freshness boundary for evidence.

Hidden chain-of-thought is neither requested nor stored. Causal metadata is observable provenance metadata, not reasoning content.

## Evaluation / ablation design

The initial harness compares two process variants on the same frozen case:

- baseline: no required agentic loop;
- disciplined: explicit understand -> explore -> plan -> act -> verify -> review contract.

The evaluator measures:

- loop completeness;
- explicit evidence gathering;
- explicit verification;
- contradiction preservation;
- recovery discipline;
- preservation of the case's expected disposition.

A score is a process-contract diagnostic only. It is NOT a market-performance score and NOT a profitability metric.

A valid Stage 5 research conclusion requires held-out cases and must compare the baseline and disciplined variants without allowing either variant to see outcome information that would be unavailable at decision time.

## Initial mechanical result

Repository tests verify that:

- missing verification is detected;
- iteration without recovery is detected;
- an incorrect disposition fails even when the process is otherwise complete;
- the disciplined process can satisfy the contract on a frozen missing-evidence case;
- the ablation harness does not treat a process score as trading evidence.

This is NOT yet evidence that Fable-style agentic behavior improves reasoning accuracy. That question remains an explicit evaluation target for the next Stage 5 gate.

## Research note

A 2026 review of agentic-AI evaluation highlights that task-completion benchmarks alone can miss safety, cost, maintainability and workflow-integration failures. This supports keeping the Stage 5 evaluation multidimensional rather than using a single success score. [Source: Kehkashan et al., Artificial Intelligence Review, 2026.]

## Next gate

Before Stage 5 can be marked PASSED:

1. freeze a representative set of reasoning cases;
2. define baseline and disciplined traces under identical information boundaries;
3. run both variants;
4. measure reasoning-contract correctness and failure modes;
5. perform adversarial cases involving missing evidence, contradiction, tool failure and stale/future information;
6. require evidence of whether the disciplined process improves, degrades, or does not change correctness;
7. only then decide whether the agentic layer is eligible for the next stage.

No trading-performance conclusion is permitted from this gate.


## Causal information-boundary contract

The evaluation contract now explicitly represents the decision timestamp and evidence timestamps. It rejects:

- evidence timestamped after the decision;
- malformed timestamps;
- evidence supplied without a decision timestamp;
- evidence older than the declared freshness boundary.

This makes the stale/future-information adversarial requirement testable rather than relying on strings such as "future outcome". The contract remains process-level and does not infer market outcomes.

## Frozen Stage 5 evaluation cases

The frozen ablation set contains four synthetic reasoning-contract cases:

1. missing evidence -> WAIT;
2. unresolved contradiction -> MONITOR;
3. tool failure requiring bounded recovery -> WAIT;
4. freshness-boundary verification -> WAIT.

Baseline and disciplined traces use the same decision/evidence time boundary. The cases are not market data and cannot establish profitability.

## Current gate state

The representative case set and causal adversarial tests are now committed. The repository-level Stage 5 CI result for the latest evaluation commit still requires observable workflow confirmation; Stage 5 therefore remains PENDING and is not marked PASSED.

The pass decision requires successful repository test execution plus the frozen ablation results, followed by explicit confirmation that the disciplined process improves, degrades, or does not change the measured correctness/failure profile. No Stage 6 work should begin before that gate is closed.
