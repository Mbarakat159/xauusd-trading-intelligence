# Implementation Roadmap

This roadmap protects the project from premature integration.

## Stage 1 — Evaluation foundation
Status: implemented.
- Evaluation architecture
- Baselines
- Decision log
- Case schema
- Deterministic feature-layer specification

## Stage 2 — Regime + feature contracts
Next.
- exact feature definitions;
- causality/edge-case test specification;
- probabilistic regime contract;
- regime evaluation cases;
- data-quality and freshness contract.

Exit gate: no ambiguous feature definitions and no untested regime dependency.

## Stage 3 — Initial knowledge set
Target: 30–50 high-quality knowledge objects, not hundreds.
Coverage:
- structure;
- price action;
- liquidity/auction;
- volume/order-flow with venue limits;
- volatility;
- MTF;
- macro/event;
- risk/execution;
- evidence/robustness.

Every object must have claim status, provenance, applicability, failure modes, operational definition and evaluation test.

Exit gate: every object is traceable and no unsupported rule is promoted.

## Stage 4 — Reasoning engine
Implement the reasoning constitution as an auditable state machine:
observe -> qualify evidence -> generate hypotheses -> select methods -> challenge -> invalidate -> risk/execution checks -> action.

No autonomous knowledge mutation during evaluation.

Exit gate: passes adversarial cases and preserves an immutable decision record.

## Stage 5 — Agentic/Fable layer
Add planning, tool selection, verification, recovery and bounded iteration only after the core reasoning layer works.

Each agentic capability is tested by ablation against the same cases.

Exit gate: measurable incremental value without increased unsupported claims or risk violations.

## Stage 6 — Forward shadow
Collect live observations from the actual target feed. Record TRADE, WAIT, MONITOR and BLOCK decisions and opportunity cost.

No live execution.

Exit gate: predefined sample/time and quality thresholds are met. Thresholds are fixed before reading results.

## Stage 7 — Integration proposal
Only after stages 1–6:
- stable API/schema;
- versioned knowledge package;
- read-only integration first;
- explicit risk firewall;
- watchdog/kill switch;
- open-position management;
- rollback/version pinning.

The existing autonomous-xauusd-agent remains untouched until this gate is passed.
