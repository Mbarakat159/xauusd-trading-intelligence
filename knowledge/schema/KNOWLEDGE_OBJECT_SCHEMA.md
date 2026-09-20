# Knowledge Object Schema

The knowledge base stores reusable analytical knowledge as bounded objects.

## Object types
- concept
- method
- hypothesis
- constraint
- observation
- source
- relationship
- evaluation_case

## Required fields
- id
- type
- title
- definition
- observable_inputs
- applicable_regimes
- data_requirements
- limitations
- failure_modes
- evidence_refs
- status

## Recommended fields
- derived_features
- time_horizons
- relationships
- hypotheses
- invalidation
- competing_interpretations
- evaluation_tests
- provenance
- confidence_dimensions
- last_reviewed

## Evidence boundary
Each object distinguishes:
1. direct observation
2. derived measurement
3. model interpretation
4. framework hypothesis
5. empirical research claim
6. practitioner or marketing claim

These levels must not be silently promoted into one another.

## Applicability
Every method states when it is useful, when it is weak, what data it needs, and what it cannot prove.

## Provenance
Research-backed objects retain source references and context such as instrument/venue, timeframe, sample period, assumptions and limitations.

## Contradictions
Contradictory evidence is a first-class relationship and is never overwritten by the latest source.

## Decision safety
Knowledge objects describe reasoning inputs and boundaries. They do not directly authorize orders or position sizes.
