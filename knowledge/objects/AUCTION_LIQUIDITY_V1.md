# Auction & Liquidity Knowledge Objects V1

## K019 Auction / Balance
- type: concept
- definition: A state where price repeatedly trades around an accepted area without persistent directional migration.
- operational_definition: Require predefined location and persistence/rotation criteria.
- observable_inputs: price path, range position, activity proxies, session state.
- data_requirements: causal intraday data.
- applicable_conditions: non-directional and transitional states.
- weak_conditions: event windows and rapidly migrating markets.
- failure_modes: calling every sideways segment a balance.
- competing_interpretations: pause within trend, accumulation/distribution hypothesis, simple compression.
- evidence_refs: REGIME_CONTRACT_V1
- claim_status: CLAIMED
- evaluation_tests: range/breakout transition cases.
- decision_safety: descriptive state.

## K020 Liquidity
- type: concept
- definition: The market's ability to transact size with limited price impact, which cannot be directly inferred from a single price chart.
- operational_definition: Specify venue, depth/quote data and measurement horizon when making a liquidity claim.
- observable_inputs: spread, depth, trade data where available, price impact proxies.
- data_requirements: venue-specific microstructure data for direct claims.
- applicable_conditions: execution and microstructure analysis.
- weak_conditions: broker-only XAUUSD feeds without depth.
- failure_modes: equating volume with liquidity; inferring centralized depth from OTC spot.
- competing_interpretations: activity may rise while executable liquidity deteriorates.
- evidence_refs: GOLD_DATA_DOMAIN_V1, DATA_QUALITY_CONTRACT
- claim_status: CLAIMED
- evaluation_tests: missing-order-flow case, execution deterioration.
- decision_safety: venue-specific; unknown if required data absent.

## K021 Liquidity Proxy
- type: concept
- definition: A measurable variable used as an imperfect proxy for liquidity or activity.
- operational_definition: Name the proxy, venue, transformation and known bias.
- observable_inputs: spread, tick activity, quote updates, realized volatility, depth where available.
- data_requirements: explicit provenance.
- applicable_conditions: when direct liquidity data unavailable.
- weak_conditions: cross-venue inference.
- failure_modes: proxy treated as ground truth.
- competing_interpretations: activity can reflect news rather than liquidity.
- evidence_refs: G004, K020
- claim_status: CLAIMED
- evaluation_tests: proxy-vs-direct-data tests where available.
- decision_safety: label as proxy in every downstream record.

## K022 Auction Location
- type: concept
- definition: The market's current location relative to an accepted or reference area.
- operational_definition: Reference area and location metric must be fixed before decision.
- observable_inputs: price, reference areas, range position.
- data_requirements: causal price data.
- applicable_conditions: auction/regime reasoning.
- weak_conditions: unstable reference areas.
- failure_modes: retrospective anchoring.
- competing_interpretations: acceptance, rejection, migration.
- evidence_refs: K019, K017
- claim_status: CLAIMED
- evaluation_tests: location-shift and transition cases.
- decision_safety: context only.
