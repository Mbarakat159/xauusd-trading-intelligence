# Knowledge-to-Evaluation Matrix V1

This matrix tests whether knowledge objects improve reasoning correctness without making historical profitability claims.

## Object coverage

| Object | Primary adversarial tests | Deterministic requirement | Reasoning requirement |
|---|---|---|---|
| K001 Market State | A, C, D, H | causal state assembly; missing/conflict propagation | do not collapse UNKNOWN/conflict |
| K002 Trend | A, B | confirmed swing/causal structure | do not infer persistence from future |
| K003 Range/Balance | B, G | causal location + persistence criteria | distinguish balance from pause |
| K004 Volatility Regime | B, D, F | causal volatility baseline | separate shock/transition |
| K005 Liquidity Proxy | C, F | provenance/proxy metadata | never promote proxy to direct fact |
| K006 Structural Break | A, D, E | confirmed reference + fixed break criterion | competing break interpretations |
| K007 Rejection | A, D, E | fixed reference/horizon | no post-outcome naming |
| K008 Displacement | B, D | fixed volatility baseline/threshold | no institutional-intent inference |
| K009 MTF Context | A, B, H | MTF synchronization | no timeframe voting |
| K010 Invalidation | E, G, H | predeclared observable condition | distinguish UNKNOWN from contradiction |
| K011 Stop Efficiency | F, H | explicit invalidation/execution inputs | do not optimize stop independently of thesis |
| K012 Evidence Conflict | A, C, E | provenance/conflict preservation | no averaging away disagreement |
| K013 Swing Structure | A, B | confirmation delay | no hindsight pivots |
| K014 HH/HL Sequence | A, B | causal swing comparison | preserve transition uncertainty |
| K015 Break of Structure | A, D, E | fixed level/break rule | competing break interpretations |
| K016 Sweep/Liquidity Test | C, D, E | exact excursion definition | never infer intent |
| K017 Acceptance/Rejection | A, B, D | fixed observation window | distinguish temporary interaction |
| K018 Displacement | B, D | fixed volatility baseline | event vs ordinary expansion |
| K019 Auction/Balance | B, G | versioned state criteria | avoid labeling every range |
| K020 Liquidity | C, F, H | provenance/venue contract | UNKNOWN without direct data |
| K021 Liquidity Proxy | C, F | proxy metadata | never promote proxy to fact |
| K022 Auction Location | A, B | reference causality | context, not signal |
| K023 Volatility | B, D, F | causal baseline | separate event shock |
| K024 Session State | D, H | timezone/calendar tests | session is context |
| K025 Event Risk | D, H | event timestamp integrity | constrain interpretation when reliable |
| K026 Evidence Independence | A, E | provenance/dependence graph | no evidence counting |
| K027 Disconfirmation | E, G, H | predeclared test | measurable falsification |
| K028 Robustness | all component tests | frozen perturbations | reject fragile conclusions |
| K029 Timeframe Role | A, H | timestamp/closed-bar contract | role is contextual, not dominant |
| K030 Cross-Timeframe Structural Alignment | A, B, E | synchronized state comparison | preserve conflict/transition states |
| K031 Timeframe Transition | B, E, H | causal confirmation | distinguish transition from retracement |
| K032 Context Nesting | A, B | hierarchy consistency | no timeframe vote counting |
| K033 Event Pre-Window | D, H | event timestamp/timezone integrity | no post-event leakage |
| K034 Event Shock Separation | D, H | event-window labeling | separate shock from ordinary expansion |
| K035 Session Transition | D, H | timezone/DST/calendar tests | session is contextual |
| K036 Volume Evidence Class | C, F, H | venue/source provenance | do not overinterpret measurement |
| K037 Tick Activity Proxy | C, F | proxy metadata | never promote proxy to centralized volume |
| K038 Centralized Order-Flow Evidence | C, F, H | venue/field validation | keep claims venue-scoped |
| K039 Volume Divergence | C, D, E | predeclared divergence definition | competing explanations required |
| K040 Order-Flow Data Sufficiency | C, F, H | capability matrix | UNKNOWN or narrowed claim when insufficient |

## Cross-cutting schema gate

Every K/G knowledge object must expose the required authoring fields:
definition, operational_definition, observable_inputs, data_requirements, applicable_conditions, weak_conditions, failure_modes, competing_interpretations, evidence_refs, claim_status, evaluation_tests and decision_safety.

Every object must also:
- reference canonical feature/data contracts where measurements are involved;
- preserve UNKNOWN when required inputs are absent;
- use only information available at the decision cutoff;
- expose material competing interpretations;
- remain analytical rather than encoding a universal entry/exit rule.

## Relationship/graph regression gate

Changes to the relationship graph must be tested for:
- missing required-data edges;
- accidental evidence double-counting;
- loss of competing interpretations;
- broken provenance links;
- contradiction/UNKNOWN preservation;
- accidental timeframe majority voting;
- accidental proxy-to-direct-data promotion.

## Evaluation separation

- Historical/synthetic cases: correctness, causality and anti-leakage only.
- Forward shadow: trading-quality evidence.
- No historical case result is treated as proof of live XAUUSD profitability.
