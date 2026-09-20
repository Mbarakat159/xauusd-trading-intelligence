# Knowledge Object Schema V2

The knowledge base stores reusable analytical knowledge as bounded, versioned objects. This document is the **canonical authoring schema** for the knowledge layer. Evaluation matrices, audits, relationship graphs, and reasoning components must reference this contract rather than maintaining a competing required-field list.

## Object types

- concept
- method
- hypothesis
- constraint
- observation
- source
- relationship
- evaluation_case

## Canonical required fields

Every analytical knowledge/data-domain object (K/G) must expose all of the following fields:

| Field | Requirement | Purpose |
|---|---|---|
| `id` | REQUIRED | Stable object identifier (for example K001 or G001). |
| `type` | REQUIRED | Object type from the controlled vocabulary above. |
| `title` | REQUIRED | Human-readable object name. |
| `definition` | REQUIRED | What the object means conceptually. |
| `operational_definition` | REQUIRED when the object is measurable/observable; otherwise explicitly `not_applicable` with rationale | How the concept is identified without hindsight. |
| `observable_inputs` | REQUIRED | Inputs that may be observed or retrieved at decision time. |
| `data_requirements` | REQUIRED | Required data, venue/source assumptions, and capability dependencies. |
| `applicable_conditions` | REQUIRED | Conditions/regimes/contexts where the object is intended to be considered. |
| `weak_conditions` | REQUIRED | Conditions under which interpretation is degraded or should be narrowed. |
| `failure_modes` | REQUIRED | Known ways the object can mislead, fail, or be unavailable. |
| `competing_interpretations` | REQUIRED | Material alternative explanations. Use an explicit empty/not-applicable value only when justified. |
| `evidence_refs` | REQUIRED | Traceable references supporting the object. |
| `claim_status` | REQUIRED | Explicit epistemic status of the claims made by the object. |
| `evaluation_tests` | REQUIRED | Tests/cases used to evaluate correctness, robustness, causality, or evidence quality. |
| `decision_safety` | REQUIRED | What the object may/cannot authorize; must preserve UNKNOWN and data/proxy limits. |

### Canonical epistemic status

`claim_status` must distinguish at least:

- `claimed` — documented claim/framework statement; not independently established here.
- `corroborated` — supported by multiple credible/independent sources, without implying live trading validity.
- `tested_on_our_data` — evaluated on our data for the stated test purpose; does not by itself establish profitability.
- `forward_supported` — supported by forward/live-shadow evidence under the stated scope and evaluation protocol.

A higher status must never be assigned merely because more sources or indicators agree. Promotion requires the applicable evidence gate.

## Controlled legacy aliases

Older authoring documents may use these names:

- `applicable_regimes` -> canonical `applicable_conditions`
- `limitations` -> represented through `weak_conditions` and/or `failure_modes`
- `status` -> canonical `claim_status`

These aliases are compatibility mappings, **not alternative schema definitions**. New objects must use canonical names. Existing objects may retain an alias temporarily only if the canonical field is also present and the mapping is explicit.

## Recommended / conditional fields

These are useful but are not substitutes for required fields:

- `derived_features`
- `time_horizons`
- `relationships`
- `hypotheses`
- `invalidation`
- `provenance`
- `confidence_dimensions`
- `last_reviewed`
- `version`
- `source_scope`

## Evidence boundary

Each object distinguishes, where applicable:

1. direct observation
2. derived measurement
3. model interpretation
4. framework hypothesis
5. empirical research claim
6. practitioner or marketing claim

These levels must not be silently promoted into one another.

## Operational-definition rules

Operational definitions must:

- be causal and usable without future bars/outcomes;
- reference versioned deterministic feature/data contracts when measurement is involved;
- state confirmation windows or parameters where relevant;
- preserve missing, stale, invalid, conflicting, or unavailable inputs as UNKNOWN/quality states;
- avoid universal trading thresholds unless the threshold is explicitly part of a versioned evaluation configuration;
- never encode a universal entry, exit, TP, SL, lot-size, or position-sizing rule.

## Applicability and limitations

Every object states when it is useful, when it is weak, what data it needs, and what it cannot prove. Context is not evidence by itself.

## Provenance

Research-backed objects retain traceable source references and, where relevant, instrument/venue, timeframe, sample period, assumptions, and limitations.

## Contradictions and UNKNOWN

Contradictory evidence is first-class information and is never overwritten by the latest source. Missing relationships or unavailable data remain UNKNOWN; they are not inferred into positive evidence.

## Decision safety

Knowledge objects provide reasoning inputs and boundaries. They do not directly authorize orders, position sizes, or live execution.

## Schema governance

This V2 schema is the single source of truth for knowledge-object authoring. Any audit or evaluation document that lists required fields must match this contract exactly. Changes require a versioned schema update and re-audit of the knowledge layer.
