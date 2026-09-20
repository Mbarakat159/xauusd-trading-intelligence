# Knowledge Relationship Graph V1

Purpose: make knowledge retrieval contextual rather than keyword or indicator voting.

## Core relationships

- K013 Swing Structure -> supports -> K014 Higher High / Higher Low Sequence
- K013 Swing Structure -> supports -> K015 Break of Structure
- K015 Break of Structure -> alternative_to -> K017 Acceptance / Rejection
- K016 Sweep / Liquidity Test -> requires_data -> K020 Liquidity
- K016 Sweep / Liquidity Test -> useful_in -> K019 Auction / Balance
- K017 Acceptance / Rejection -> supports -> K022 Auction Location
- K018 Displacement -> supports -> K023 Volatility Expansion / Compression
- K019 Auction / Balance -> useful_in -> K022 Auction Location
- K020 Liquidity -> requires_data -> venue-specific depth/quote/trade data
- K021 Liquidity Proxy -> alternative_to -> K020 Liquidity when direct data are unavailable
- K021 Liquidity Proxy -> weak_in -> direct-liquidity claims
- K023 Volatility Expansion / Compression -> supports -> K025 Event Risk State
- K024 Session State -> contextualizes -> K023 Volatility Expansion / Compression
- K025 Event Risk State -> constrains -> K018 Displacement
- K025 Event Risk State -> constrains -> K023 Volatility Expansion / Compression
- K026 Evidence Independence -> constrains -> K027 Disconfirmation Test
- K026 Evidence Independence -> contradicts -> indicator-voting logic
- K027 Disconfirmation Test -> tests -> K015 Break of Structure
- K027 Disconfirmation Test -> tests -> K016 Sweep / Liquidity Test
- K028 Robustness -> constrains -> all operational promotion
- G004 Tick Activity Proxy -> supports -> K021 Liquidity Proxy
- G002 CME/COMEX Gold Futures -> requires_data -> venue-specific microstructure claims
- G001 Broker XAUUSD Feed -> weak_in -> centralized order-flow claims

## Retrieval rule

A downstream reasoning component should retrieve:
1. the concept itself;
2. its required data;
3. competing interpretations;
4. known weak conditions;
5. relevant disconfirmation tests;
6. applicable regime/session/event context;
7. evidence provenance and claim status.

A missing relationship is UNKNOWN, not an invitation to infer one.

## Safety rule

No relationship in this graph is a trading signal. Relationships describe analytical dependencies and evidence constraints.
