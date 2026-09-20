# Knowledge Objects — MTF, Context, Volume & Order Flow V1

## Scope

These objects extend the knowledge layer without defining a fixed trading strategy. They describe how an intelligence system may interpret multi-timeframe context, event/session state, volume and order-flow evidence, and the limits of those observations.

## K029 — Timeframe Role
- type: contextual_reasoning
- title: Timeframe Role
- definition: A timeframe is an observation scale with a particular temporal resolution; its analytical role depends on the question being asked rather than on a universal hierarchy.
- operational_definition: For each observation, record timeframe, timestamp, sampling interval, and the analytical question assigned to that timeframe. Do not infer importance from timeframe label alone.
- observable_inputs: timeframe, OHLC, timestamp, derived structure/volatility features.
- data_requirements: synchronized multi-timeframe price data with explicit bar-close timestamps.
- applicable_conditions: multi-scale market analysis.
- weak_conditions: unsynchronized feeds, missing bars, ambiguous session boundaries.
- failure_modes: treating a timeframe as inherently dominant; mixing closed-bar and incomplete-bar observations.
- competing_interpretations: higher timeframe may describe broader context while lower timeframe describes local execution structure; neither is automatically a trading signal.
- evidence_refs: internal research/MTF_REASONING.md.
- claim_status: conceptual / architecture-supported; not a profitability claim.
- evaluation_tests: timestamp causality; closed-bar integrity; same-state comparison across resolutions; no hidden future bars.
- decision_safety: timeframe role may contextualize evidence but cannot by itself authorize an action.

## K030 — Cross-Timeframe Structural Alignment
- type: contextual_reasoning
- title: Cross-Timeframe Structural Alignment
- definition: Alignment exists when structural observations from different timeframes describe compatible state relationships without requiring identical direction.
- operational_definition: Compare explicitly defined structural states across selected timeframes and classify the relationship as aligned, nested, conflicting, transitional, or UNKNOWN.
- observable_inputs: swing structure, break/acceptance state, volatility state, timeframe role.
- data_requirements: synchronized multi-timeframe observations.
- applicable_conditions: MTF state interpretation.
- weak_conditions: different confirmation delays, sparse lower-timeframe data, rapidly transitioning markets.
- failure_modes: majority voting; demanding universal agreement; treating disagreement as automatic reversal evidence.
- competing_interpretations: lower-timeframe counter-movement can be retracement, transition, or independent structure.
- evidence_refs: internal research/MTF_REASONING.md.
- claim_status: conceptual / testable.
- evaluation_tests: adversarial MTF-conflict cases; transition cases; no future-state leakage.
- decision_safety: disagreement must remain explicit; it is not a signal by itself.

## K031 — Timeframe Transition
- type: market_state
- title: Timeframe Transition
- definition: A timeframe transition occurs when structural or volatility state changes enough that previously valid contextual relationships may no longer describe the current market.
- operational_definition: Detect a state change using timestamped deterministic observations and retain the previous state until the defined confirmation condition is met.
- observable_inputs: structure changes, volatility changes, acceptance/rejection, session/event context.
- data_requirements: causal sequential observations.
- applicable_conditions: regime or structure change analysis.
- weak_conditions: noisy short samples, event shocks, feed gaps.
- failure_modes: hindsight relabeling; declaring transition from a single unconfirmed movement.
- competing_interpretations: ordinary retracement, temporary volatility expansion, genuine structural transition.
- evidence_refs: internal research/MTF_REASONING.md; research/taxonomy/REGIME_CONTRACT_V1.md.
- claim_status: conceptual / testable.
- evaluation_tests: causal transition labeling; confirmation delay; transition adversarial cases.
- decision_safety: transition state should increase uncertainty until confirmation, not automatically change direction.

## K032 — Context Nesting
- type: contextual_reasoning
- title: Context Nesting
- definition: A lower-resolution observation can be interpreted inside a broader state without requiring the lower-resolution state to match the broader state.
- operational_definition: Represent each timeframe state as a child observation linked to a parent contextual state, with explicit timestamps and relationship type.
- observable_inputs: MTF structure, volatility, auction/balance state.
- data_requirements: synchronized timeframe hierarchy.
- applicable_conditions: multi-scale interpretation.
- weak_conditions: incompatible sampling intervals or missing parent observations.
- failure_modes: flattening all timeframes into one vote; assuming parent state determines child behavior.
- competing_interpretations: lower timeframe may be continuation, retracement, local balance, or transition within broader context.
- evidence_refs: internal research/MTF_REASONING.md.
- claim_status: conceptual / architectural.
- evaluation_tests: nesting consistency; contradiction preservation; no majority-vote behavior.
- decision_safety: nesting is descriptive context only.

## K033 — Event Pre-Window
- type: event_context
- title: Event Pre-Window
- definition: The period before a scheduled market-moving event during which ordinary observations may be affected by anticipation, positioning changes, reduced liquidity, or altered participation.
- operational_definition: Derive from an authoritative event timestamp and a versioned pre-event window definition; do not infer the window from price movement.
- observable_inputs: event timestamp, event category, scheduled status, market/session timestamp.
- data_requirements: reliable event calendar with timezone and revision metadata.
- applicable_conditions: scheduled macro/news analysis.
- weak_conditions: unscheduled news, stale calendars, uncertain release times.
- failure_modes: treating every event as equally important; using post-event information to classify pre-event state.
- competing_interpretations: observed compression may be ordinary balance, session effect, or event anticipation.
- evidence_refs: internal research/gold/EVENT_SESSION_MODEL.md.
- claim_status: conceptual / data-contract dependent.
- evaluation_tests: event timestamp integrity; timezone conversion; pre/post boundary causality.
- decision_safety: reliable pre-event state can constrain interpretation; it does not predict event direction.

## K034 — Event Shock Separation
- type: event_context
- title: Event Shock Separation
- definition: Price/volatility behavior immediately surrounding a material event should be distinguished from ordinary market-state observations because the event may be an external state change.
- operational_definition: Mark observations by event proximity and compare event-window behavior separately from non-event observations using only information available at each timestamp.
- observable_inputs: event timestamps, price movement, volatility, session state.
- data_requirements: event calendar plus market timestamps.
- applicable_conditions: macro-sensitive periods.
- weak_conditions: incomplete event metadata; multiple overlapping events.
- failure_modes: attributing all displacement to event causality; ignoring ordinary structure; leaking release outcome into pre-event reasoning.
- competing_interpretations: event-driven shock, ordinary volatility expansion, session transition, liquidity change.
- evidence_refs: internal research/gold/EVENT_SESSION_MODEL.md.
- claim_status: conceptual / testable.
- evaluation_tests: event-vs-non-event separation; leakage checks; overlapping-event cases.
- decision_safety: event proximity may constrain confidence and interpretation, not establish direction.

## K035 — Session Transition
- type: session_context
- title: Session Transition
- definition: A session transition is a time boundary at which the participant mix, liquidity conditions, or activity characteristics may change.
- operational_definition: Identify session boundaries from a versioned timezone/calendar definition and preserve the boundary as metadata rather than inferring it from price.
- observable_inputs: timestamp, session calendar, volatility/activity features.
- data_requirements: timezone-aware market calendar.
- applicable_conditions: intraday analysis.
- weak_conditions: broker server-time changes, holidays, daylight-saving transitions.
- failure_modes: hard-coded UTC offsets; treating session labels as deterministic directional predictors.
- competing_interpretations: activity change may arise from session transition, event risk, or independent volatility.
- evidence_refs: internal research/gold/EVENT_SESSION_MODEL.md.
- claim_status: conceptual / calendar-dependent.
- evaluation_tests: DST/holiday tests; timezone conversion; session-boundary causality.
- decision_safety: session state is context and may constrain interpretation; it is not a signal.

## K036 — Volume Evidence Class
- type: evidence
- title: Volume Evidence Class
- definition: Volume is an observed measure whose meaning depends on the venue, instrument, aggregation method, and data source.
- operational_definition: Every volume observation must carry venue, instrument, source, aggregation interval, and whether it represents trades, reported volume, or broker activity.
- observable_inputs: volume, venue, instrument, timestamp, aggregation.
- data_requirements: provenance-aware volume feed.
- applicable_conditions: volume-based analysis.
- weak_conditions: OTC/CFD feeds without centralized volume.
- failure_modes: treating tick count as exchange volume; comparing incomparable venues without normalization.
- competing_interpretations: volume expansion may reflect participation, event activity, quote updates, or feed-specific behavior.
- evidence_refs: internal research/gold/GOLD_MICROSTRUCTURE.md; research/gold/DATA_CAPABILITY_MAP.md.
- claim_status: conceptual / data-provenance dependent.
- evaluation_tests: provenance enforcement; venue mismatch tests; missing-volume UNKNOWN tests.
- decision_safety: volume cannot be interpreted beyond what the source actually measures.

## K037 — Tick Activity Proxy
- type: proxy
- title: Tick Activity Proxy
- definition: Tick count or broker activity can be used as a proxy for local feed activity, but it is not centralized market volume or order flow.
- operational_definition: Store tick/activity observations with broker/feed identity and explicitly label them as proxy measurements.
- observable_inputs: tick count/activity, broker feed, timestamp.
- data_requirements: broker tick stream.
- applicable_conditions: monitoring local feed activity when direct centralized volume is unavailable.
- weak_conditions: feed-specific aggregation, quote-generation differences, cross-broker comparison.
- failure_modes: upgrading proxy to factual participation or liquidity; inferring hidden orders or intent.
- competing_interpretations: activity may reflect quoting behavior rather than executed volume.
- evidence_refs: internal research/gold/GOLD_MICROSTRUCTURE.md; research/gold/DATA_CAPABILITY_MAP.md.
- claim_status: proxy / not direct order-flow evidence.
- evaluation_tests: metadata preservation; broker-change sensitivity; UNKNOWN when source is missing.
- decision_safety: proxy may contextualize observations but cannot establish centralized liquidity or participant intent.

## K038 — Centralized Order-Flow Evidence
- type: evidence
- title: Centralized Order-Flow Evidence
- definition: Direct order-flow claims require a venue-specific source capable of observing the relevant trades, quotes, depth, or other defined market microstructure fields.
- operational_definition: A claim is classified as direct only when the data source and venue explicitly provide the required measurement; otherwise classify as indirect/proxy/UNKNOWN.
- observable_inputs: venue, trades, quotes, depth, aggressor classification where available.
- data_requirements: identified venue-specific market data.
- applicable_conditions: futures or other centralized-market analysis where appropriate data are available.
- weak_conditions: fragmented markets; delayed or partial feeds.
- failure_modes: treating CFD/broker ticks as centralized order flow; mixing venues without labeling.
- competing_interpretations: direct venue evidence describes that venue, not automatically the entire global gold market.
- evidence_refs: internal research/gold/GOLD_MICROSTRUCTURE.md; research/gold/DATA_CAPABILITY_MAP.md.
- claim_status: methodological / venue-dependent.
- evaluation_tests: venue/source validation; field availability; cross-venue attribution tests.
- decision_safety: direct evidence must remain venue-scoped and cannot establish universal market intent.

## K039 — Volume Divergence
- type: contextual_evidence
- title: Volume Divergence
- definition: Volume divergence describes a mismatch between a defined price/structure observation and a defined volume measurement; it is an observation requiring competing explanations.
- operational_definition: Define both price condition and volume condition before inspection, then record the divergence without assigning causal meaning.
- observable_inputs: price structure, volume class, timestamp.
- data_requirements: comparable price and volume observations with provenance.
- applicable_conditions: venue-valid volume analysis.
- weak_conditions: proxy volume, event windows, changing feed quality.
- failure_modes: treating divergence as reversal proof; ignoring scale or regime changes.
- competing_interpretations: participation change, aggregation artifact, event effect, ordinary continuation.
- evidence_refs: internal research/gold/GOLD_MICROSTRUCTURE.md; internal evidence model.
- claim_status: analytical observation / hypothesis-generating only.
- evaluation_tests: predeclared divergence definition; alternative explanations; event separation.
- decision_safety: divergence can generate a hypothesis but cannot independently authorize action.

## K040 — Order-Flow Data Sufficiency
- type: data_quality
- title: Order-Flow Data Sufficiency
- definition: Order-flow reasoning is data-sufficient only when the available fields support the specific claim being made.
- operational_definition: For every order-flow claim, map required fields to available fields and return SUFFICIENT, PARTIAL, or UNKNOWN.
- observable_inputs: claim type, venue, available fields, feed provenance.
- data_requirements: explicit data capability map.
- applicable_conditions: any order-flow or liquidity inference.
- weak_conditions: undocumented feeds, partial depth, delayed data.
- failure_modes: silently substituting proxies; claiming precision beyond the data.
- competing_interpretations: partial data may support a narrower claim but not the original claim.
- evidence_refs: internal research/gold/DATA_CAPABILITY_MAP.md.
- claim_status: methodological / deterministic contract.
- evaluation_tests: capability matrix; missing-field cases; proxy substitution rejection.
- decision_safety: insufficient data must produce UNKNOWN or a narrowed claim, never fabricated certainty.
