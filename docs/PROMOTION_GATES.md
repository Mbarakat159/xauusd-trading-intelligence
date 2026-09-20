# Promotion Gates

These gates prevent the project from becoming a large unvalidated system.

## Gate 0 — Research integrity
Pass when:
- sources are traceable;
- claims are status-labeled;
- unsupported marketing claims are restricted;
- contradictions are retained.

## Gate 1 — Measurement integrity
Pass when:
- deterministic features have exact definitions;
- causality is tested;
- missing/stale data is explicit;
- feature versions are immutable.

## Gate 2 — Reasoning integrity
Pass when:
- the reasoning constitution is followed;
- raw observations are separated from interpretations;
- hypotheses include invalidation;
- contradictions are preserved;
- no unsupported evidence is invented.

## Gate 3 — Component evaluation
Pass when regime, method selection, invalidation and risk construction pass predefined adversarial cases.

## Gate 4 — Baseline evaluation
Pass only if incremental complexity demonstrates predefined benefits versus frozen controls under identical information.

## Gate 5 — Forward shadow
Pass only after a predefined forward observation window and sample threshold, with decisions recorded before outcomes.

## Gate 6 — Integration safety
Before connecting to the autonomous agent:
- read-only integration first;
- version pinning;
- rollback;
- deterministic risk firewall;
- stale-data block;
- broker/account reconciliation;
- independent watchdog;
- kill switch;
- open-position management.

## No-pass rule
If a gate fails, do not bypass it by adding more knowledge, changing metrics after seeing results, or connecting the live agent early.
