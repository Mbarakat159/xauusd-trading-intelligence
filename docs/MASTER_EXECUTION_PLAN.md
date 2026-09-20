# MASTER EXECUTION PLAN — XAUUSD Trading Intelligence

Status: ACTIVE / FROZEN SCOPE
Last updated: 2026-09-20
Repository: Mbarakat159/xauusd-trading-intelligence

## 1. Mission

Build an independent, versioned XAUUSD market-intelligence layer that can later be connected to the autonomous trading agent.

This repository is NOT the live execution agent.

The intelligence layer must learn/reason from broad professional market-analysis knowledge without being hard-coded to one trading strategy.

## 2. Non-negotiable project rules

1. Do not modify the separate `autonomous-xauusd-agent` repository unless the user explicitly authorizes integration.
2. Do not silently change the architecture, sequence, evaluation criteria, or scope.
3. Do not invent missing facts, evidence, data, capabilities, or results.
4. UNKNOWN remains UNKNOWN when evidence is unavailable.
5. No fixed entry/exit strategy is to be hard-coded into the intelligence layer.
6. No indicator-majority voting.
7. No requirement that all timeframes agree.
8. MTF is contextual/relational, not vote counting.
9. LLM confidence is not calibrated probability of profit.
10. Broker tick activity is not treated as centralized order flow.
11. Venue-specific claims must identify the venue/data source.
12. No historical/backtest result is presented as proof of live XAUUSD profitability.
13. Historical/synthetic cases are for correctness, causality, leakage, and adversarial reasoning tests.
14. Trading-quality claims require forward/shadow evidence.
15. Decisions must be timestamped and immutable before outcome visibility.
16. WAIT/BLOCK outcomes must be evaluated for both avoided exposure and opportunity cost.
17. Risk/execution hard constraints must remain deterministic and outside free-form LLM reasoning.
18. No online self-modification of trading rules, risk limits, feature definitions, knowledge claims, or sizing.
19. Changes follow: proposal -> review -> isolated test -> frozen comparison -> forward shadow -> promotion/rejection.
20. Any change to this master plan requires explicit user approval.

## 3. Architecture sequence — fixed

RAW MARKET DATA
-> DATA VALIDATION
-> DETERMINISTIC FEATURES
-> E0/E1 OBSERVATIONS
-> MARKET REGIME
-> METHOD SELECTION
-> KNOWLEDGE RETRIEVAL
-> COMPETING HYPOTHESES
-> DISCONFIRMATION
-> INVALIDATION
-> RISK / EXECUTION
-> TRADE / WAIT / MONITOR / BLOCK
-> OUTCOME
-> EVALUATION

## 4. Fixed implementation stages

### Stage 1 — Evaluation Foundation
Status: IMPLEMENTED
Includes:
- evaluation architecture
- baselines
- decision schema
- case schema
- anti-leakage rules
- forward-vs-historical separation

### Stage 2 — Data + Deterministic Observation
Status: PASSED / IMPLEMENTED
Includes:
- deterministic feature definitions
- feature contracts
- feature test plan
- data-quality contract
- gold data-domain separation
- regime contract
- method-selection contract

Do not build reasoning on undefined measurements.

Stage 2 gate evidence: evaluation/STAGE2_VALIDATION_REPORT_V1.md

### Stage 3 — Knowledge Layer
Status: PASSED / IMPLEMENTED
Target: approximately 30–50 high-quality knowledge objects.
Each object must contain:
- definition
- operational definition
- observable inputs
- data requirements
- applicable conditions
- weak conditions
- failure modes
- competing interpretations
- evidence references
- claim status
- evaluation tests
- decision safety

Knowledge is contextual, relational, and provenance-aware.

### Stage 4 — Reasoning Engine
NOT STARTED.
Only begin after Stage 3 definitions are sufficiently complete and frozen.

Required behavior:
1. establish observable state
2. separate observations from interpretations
3. identify missing evidence
4. generate multiple hypotheses
5. retrieve relevant analytical families
6. evaluate support and contradiction
7. search for measurable disconfirmation
8. define invalidation
9. evaluate execution/event/liquidity/risk constraints
10. choose TRADE / WAIT / MONITOR / BLOCK
11. write immutable decision record

No live execution.

### Stage 5 — Fable / Agentic Reasoning Layer
NOT STARTED.
Use Fable research only for agentic reasoning/tool-use principles.
Do not copy a leaked prompt blindly.
Ablate/test whether agentic principles improve reasoning correctness.
No trading rules are imported merely because they appear in Fable material.

### Stage 6 — Decision / Risk / Execution Safety
NOT STARTED.
Deterministic safety layer.
Must include:
- hard risk constraints
- execution-quality checks
- exposure checks
- data/tool failure handling
- safe WAIT/BLOCK behavior
- open-position management design
- independent watchdog / kill switch
- rollback capability

### Stage 7 — Forward Shadow
NOT STARTED.
Use live/forward market observations without sending live orders.
Freeze relevant versions during evaluation windows.
Evaluate:
- reasoning correctness
- feature correctness
- regime behavior
- method selection
- decision quality
- WAIT opportunity cost
- execution assumptions
- stability
- robustness

No profitability claim before predefined evidence criteria are met.

### Stage 8 — Promotion Review
NOT STARTED.
Use explicit promotion gates:
- research integrity
- measurement integrity
- reasoning integrity
- component evaluation
- baseline comparison
- forward shadow
- integration safety

A failed gate blocks progression.

### Stage 9 — Integration Proposal
NOT STARTED.
Only after all required gates pass.
Integration with `autonomous-xauusd-agent` requires explicit user authorization.
Integration is not automatic.

## 5. Current exact position

Completed foundations:
- research plan
- source policy
- Fable research
- knowledge map
- architecture findings
- taxonomy
- trade-quality model
- methodology matrix
- regime model
- MTF reasoning
- evidence model
- risk/execution model
- source registry
- gap analysis
- evaluation foundation
- reasoning constitution
- knowledge schema
- relationship model
- deterministic feature specification
- data quality contract
- promotion gates
- safe evolution policy
- foundational knowledge objects
- gold data-domain objects
- structure/price-action objects
- auction/liquidity objects
- volatility/session/event objects
- evidence/robustness objects
- relationship graph
- knowledge evaluation matrix

Current next action:
BEGIN STAGE 4 — REASONING ENGINE only after reviewing the Stage 4 entry gate and implementation requirements.

Stage 3 gate evidence: `knowledge/KNOWLEDGE_LAYER_AUDIT_V1.md`.

Do NOT begin live execution or integration with `autonomous-xauusd-agent`.

## 6. Knowledge expansion order

Unless explicitly changed by the user, expand in this order:
A. Market structure / price action
B. Auction / liquidity / market profile
C. Volatility / regimes
D. Multi-timeframe reasoning
E. Macro / event / session context
F. Volume / order-flow limitations
G. Classical technical analysis families
H. Quantitative/statistical concepts
I. Trade construction / invalidation / stop efficiency
J. Evidence / robustness / research methodology
K. Gold-specific venue and microstructure knowledge

Objects must remain analytical knowledge, not fixed strategy rules.

## 7. Required gate before Stage 4

Before starting the Reasoning Engine, verify:
- knowledge definitions are internally consistent
- operational definitions are testable
- required data are explicit
- competing interpretations are represented
- claim statuses are explicit
- relationship graph is coherent
- evaluation matrix covers material objects
- no object silently encodes a fixed strategy
- deterministic feature contracts are sufficient for the intended reasoning tasks

If any condition fails, remain in Stage 3.

## 8. Conversation handoff protocol

If a conversation ends, the next conversation must first inspect this file and the latest repository commits before continuing.

The next conversation must treat this document as the authoritative execution plan.

It must NOT:
- restart the project
- invent a different roadmap
- skip stages
- reorder stages
- integrate with the autonomous agent
- introduce a new architecture
- reinterpret user requirements
- declare a gate passed without evidence

If the next conversation discovers a genuine architectural conflict, it must STOP at the affected point and ask the user for approval rather than silently changing the plan.

## 9. User authority rule

The user is the authority for scope changes.

The assistant may identify:
- bugs
- contradictions
- missing requirements
- safety issues
- architectural risks
- evidence gaps

But identifying a problem does NOT authorize changing the plan.

Any change to:
- stage order
- repository boundary
- architecture
- promotion gates
- evaluation philosophy
- live integration timing
- risk philosophy
- fixed project constraints

requires explicit user approval.

## 10. Continuation command

When the user says:
"كمل"

The default interpretation is:
Continue from the exact current stage and latest repository state, following this master plan, without introducing new scope.

The assistant should first inspect the latest commit/state, then execute the next unfinished task.

## 11. Progress reporting

After each meaningful stage/task:
- report exactly what was completed
- report repository commit(s)
- report current stage
- report next planned task
- identify anything blocked
- do not claim completion beyond the actual repository state

## 12. Definition of done

The project is not considered complete merely because files exist.

A stage is complete only when its defined artifacts, tests, evaluation criteria, and required review gates are satisfied.

Live trading integration is a separate final decision, never an automatic consequence of finishing the research/intelligence stages.
