# Knowledge-to-Evaluation Matrix V1

This matrix tests whether knowledge objects improve reasoning correctness without making historical profitability claims.

| Object | Primary adversarial tests | Deterministic requirement | Reasoning requirement |
|---|---|---|---|
| K013 Swing Structure | A, B | confirmation delay | no hindsight pivots |
| K014 HH/HL Sequence | A, B | causal swing comparison | preserve transition uncertainty |
| K015 Break of Structure | A, D, E | fixed level/break rule | competing break interpretations |
| K016 Sweep/Liquidity Test | C, D, E | exact excursion definition | never infer intent |
| K017 Acceptance/Rejection | A, B, D | fixed observation window | distinguish temporary interaction |
| K018 Displacement | B, D | fixed volatility baseline | event vs ordinary expansion |
| K019 Auction/Balance | B, G | state definition | avoid labeling every range |
| K020 Liquidity | C, F, H | provenance/venue contract | UNKNOWN without direct data |
| K021 Liquidity Proxy | C, F | proxy metadata | never promote proxy to fact |
| K022 Auction Location | A, B | reference causality | context, not signal |
| K023 Volatility | B, D, F | causal baseline | separate event shock |
| K024 Session State | D, H | timezone/calendar tests | session is context |
| K025 Event Risk | D, H | event timestamp integrity | hard constraint when reliable |
| K026 Evidence Independence | A, E | provenance graph | no evidence counting |
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

## Acceptance criteria

An object is not operationally promoted because a case “looks correct.” It must:
- pass its deterministic definition tests where applicable;
- preserve UNKNOWN when required inputs are missing;
- avoid future information;
- expose competing interpretations where ambiguity is material;
- identify a measurable disconfirmation test where the object supports a hypothesis;
- carry provenance and claim status;
- survive regression when the knowledge graph changes;
- remain analytical rather than becoming a universal entry/exit rule.

## Evaluation separation

- Historical/synthetic cases: correctness and anti-leakage only.
- Forward shadow: trading-quality evidence.
- No historical case result is treated as proof of live XAUUSD profitability.
