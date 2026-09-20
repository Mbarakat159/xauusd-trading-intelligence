# Knowledge Object Authoring Guide V1

## Purpose
Turn research into small, testable knowledge objects without turning the repository into a collection of trading rules.

## Required object fields
id, type, title, definition, operational_definition, observable_inputs, data_requirements, applicable_conditions, weak_conditions, failure_modes, competing_interpretations, evidence_refs, claim_status, evaluation_tests, decision_safety.

## Authoring rules
1. Separate observation from interpretation.
2. State exactly what the concept means operationally.
3. State what data it requires.
4. State what the concept cannot establish.
5. Record alternative interpretations where ambiguity exists.
6. Link every empirical claim to provenance.
7. Never encode an entry, stop, target or lot-size rule as a universal truth.
8. If a concept is venue-specific, name the venue/data domain.
9. If evidence is study-specific, keep its scope study-specific.
10. Prefer UNKNOWN over invented values.

## Promotion
A knowledge object may be used operationally only after its claim status and evaluation requirements satisfy the relevant promotion gate.
