# Safe Evolution Policy

The intelligence layer must improve without silently rewriting its own rules.

## Frozen evaluation
During a component evaluation window:
- knowledge version is frozen;
- feature version is frozen;
- model configuration is frozen;
- scoring definitions are frozen.

## Proposed change lifecycle
proposal -> review -> isolated test -> frozen comparison -> forward shadow -> promotion/rejection

## No online self-modification
The agent may record candidate improvements, but it must not autonomously promote:
- new trading rules;
- new risk limits;
- new feature definitions;
- new knowledge claims;
- new position-sizing logic.

## Regression requirement
Every promoted change must preserve previously passed invariants or explicitly version the changed behavior and rerun affected tests.

## Rollback
Every operational package must identify:
- code version;
- feature version;
- knowledge version;
- configuration version.

A failed promotion must be reversible to the previous known-good package.

## Human approval gate
Any change that can affect live orders, risk limits or broker interaction requires explicit approval before integration.

## Learning without self-deception
Post-decision outcomes can update research status, but the system must not rewrite the original decision record to make the reasoning appear correct in hindsight.
