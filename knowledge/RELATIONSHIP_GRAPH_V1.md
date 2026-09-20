# Knowledge Relationship Graph V1

Purpose: make knowledge retrieval contextual rather than keyword or indicator voting.

## Relationship semantics
Relationships describe analytical dependency/provenance, not trading signals. A relationship does not imply causal market truth unless its referenced claim is independently supported.

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
- K023 Volatility Expansion / Compression -> contextualizes -> K018 Displacement
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

## MTF hierarchy and context
- K009 MTF Context -> parent_of -> K029 Timeframe Role
- K029 Timeframe Role -> contextualizes -> K030 Cross-Timeframe Structural Alignment
- K030 Cross-Timeframe Structural Alignment -> depends_on -> K029 Timeframe Role
- K030 Cross-Timeframe Structural Alignment -> tests -> K032 Context Nesting
- K031 Timeframe Transition -> contextualizes -> K030 Cross-Timeframe Structural Alignment
- K031 Timeframe Transition -> depends_on -> causal sequential observations
- K032 Context Nesting -> complements -> K030 Cross-Timeframe Structural Alignment
- K032 Context Nesting -> specializes -> K009 MTF Context
- K032 Context Nesting -> contradicts -> timeframe majority voting

## Event/session hierarchy
- K025 Event Risk State -> parent_of -> K033 Event Pre-Window
- K033 Event Pre-Window -> contextualizes -> K034 Event Shock Separation
- K033 Event Pre-Window -> contextualizes -> K023 Volatility Expansion / Compression
- K034 Event Shock Separation -> constrains -> interpretation of K018 Displacement
- K034 Event Shock Separation -> constrains -> interpretation of K023 Volatility Expansion / Compression
- K024 Session State -> parent_of -> K035 Session Transition
- K035 Session Transition -> contextualizes -> K024 Session State
- K035 Session Transition -> contextualizes -> K023 Volatility Expansion / Compression
- K035 Session Transition -> requires_data -> timezone-aware session calendar

## Liquidity/volume hierarchy
- K005 Liquidity Proxy -> parent_of -> K021 Liquidity Proxy
- K020 Liquidity -> parent_of -> K038 Centralized Order-Flow Evidence for direct venue evidence
- K036 Volume Evidence Class -> requires_data -> venue/source provenance
- K036 Volume Evidence Class -> contextualizes -> K037 Tick Activity Proxy
- K037 Tick Activity Proxy -> alternative_to -> K038 Centralized Order-Flow Evidence when direct venue data are unavailable
- K037 Tick Activity Proxy -> weak_in -> claims about centralized participation or intent
- K038 Centralized Order-Flow Evidence -> requires_data -> venue-specific trades/quotes/depth
- K038 Centralized Order-Flow Evidence -> constrains -> K020 Liquidity
- K039 Volume Divergence -> depends_on -> K036 Volume Evidence Class
- K039 Volume Divergence -> tests -> competing interpretations
- K039 Volume Divergence -> weak_in -> unsupported causal claims
- K040 Order-Flow Data Sufficiency -> constrains -> K038 Centralized Order-Flow Evidence
- K040 Order-Flow Data Sufficiency -> constrains -> K020 Liquidity
- K040 Order-Flow Data Sufficiency -> supports -> UNKNOWN preservation
- K033 Event Pre-Window -> contextualizes -> K039 Volume Divergence
- K034 Event Shock Separation -> constrains -> K039 Volume Divergence

## Deterministic feature dependencies
- K013 -> requires_data -> F007 Confirmed Swing
- K015 -> requires_data -> F008 Structural Reference + F009 Structural Break
- K018 -> requires_data -> F005 Volatility Baseline
- K019 -> requires_data -> F006 Range Position plus versioned persistence/rotation criteria
- K020 -> requires_data -> venue-specific microstructure fields
- K021 -> requires_data -> provenance metadata
- K023 -> requires_data -> F004 Realized Volatility + F005 Volatility Baseline
- K024 -> requires_data -> F015 Session State
- K025 -> requires_data -> F014 Event Distance + F017 Event Window
- K029 -> requires_data -> F016 MTF Synchronization
- K030 -> requires_data -> F016 MTF Synchronization
- K031 -> requires_data -> versioned state-change/confirmation rule
- K033 -> requires_data -> F014 Event Distance + F017 Event Window
- K034 -> requires_data -> F017 Event Window
- K035 -> requires_data -> F015 Session State
- K036 -> requires_data -> F013 Volume Provenance
- K037 -> requires_data -> F012 Activity / Tick Proxy
- K038 -> requires_data -> F018 Proxy Capability
- K039 -> requires_data -> F013 Volume Provenance
- K040 -> requires_data -> F018 Proxy Capability

## Retrieval rule
A downstream reasoning component should retrieve:
1. the concept itself;
2. its required deterministic features/data;
3. competing interpretations;
4. known weak conditions;
5. relevant disconfirmation tests;
6. applicable regime/session/event context;
7. evidence provenance and claim status;
8. proxy/direct-data status;
9. parent/specialization relationships;
10. method compatibility and redundancy metadata where applicable.

A missing relationship is UNKNOWN, not an invitation to infer one.

## Safety rule
No relationship in this graph is a trading signal. Relationships describe analytical dependencies and evidence constraints.
