# Knowledge Relationship Model

The knowledge graph connects concepts, methods, hypotheses, evidence and constraints.

## Relationship types
- supports
- contradicts
- depends_on
- useful_in
- weak_in
- requires_data
- derived_from
- invalidated_by
- alternative_to
- complements
- conflicts_with
- tests
- sourced_from

## Why relationships matter
A flat library encourages retrieval by keyword. A relationship graph allows retrieval by decision context.

Example flow:
market_state -> useful_in -> method
method -> requires_data -> data_capability
method -> supports -> hypothesis
hypothesis -> contradicted_by -> observation
hypothesis -> invalidated_by -> condition
hypothesis -> tested_by -> evaluation_case

## Retrieval principle
Future queries should be contextual, for example:
- Which methods apply to a high-volatility transition with OHLC and tick volume?
- Which concepts require centralized futures/order-book data that is unavailable?
- What evidence contradicts this reversal hypothesis?
- Which methods have known failure modes in the current regime?
- Which evaluation cases should challenge this conclusion?

## Graph safety
Relationships are not truth by themselves. Each relationship requires provenance or an explicit status showing it is a working hypothesis.
