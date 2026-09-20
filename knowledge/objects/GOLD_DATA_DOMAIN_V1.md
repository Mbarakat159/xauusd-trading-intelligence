# Gold Data-Domain Objects V1

These objects describe data domains and provenance. They do not imply a universal gold-market representation.

## G001 — Broker XAUUSD Feed
- type: data_domain
- title: Broker XAUUSD Feed
- definition: Broker-specific spot/CFD price and execution-environment observations.
- operational_definition: Preserve broker/feed identity, timestamps, instrument and collection metadata for every observation.
- observable_inputs: broker quotes/ticks/bars and execution metadata when available.
- data_requirements: identified broker/feed source with valid timestamps.
- applicable_conditions: broker-local price observation and execution analysis.
- weak_conditions: cross-broker inference and claims about centralized market activity.
- failure_modes: treating one broker feed as the complete global gold market.
- competing_interpretations: feed differences may reflect liquidity, aggregation, latency or broker-specific pricing.
- evidence_refs: DATA_CAPABILITY_MAP.md, GOLD_MICROSTRUCTURE.md.
- claim_status: CORROBORATED as a data-domain definition.
- evaluation_tests: source identity, timestamp and cross-feed disagreement tests.
- decision_safety: broker-scoped only.

## G002 — CME/COMEX Gold Futures
- type: data_domain
- title: CME/COMEX Gold Futures
- definition: Exchange-traded gold futures venue with centralized transaction and order-book data when such feeds are actually available.
- operational_definition: Treat futures observations as venue-specific and record the exact fields/feed used; do not assume depth or aggressor data exist unless supplied.
- observable_inputs: futures trades, quotes, depth and other available venue fields.
- data_requirements: identified venue-specific market-data source.
- applicable_conditions: venue-specific volume/order-flow analysis.
- weak_conditions: delayed, partial or absent fields.
- failure_modes: generalizing futures evidence to every spot/CFD participant.
- competing_interpretations: futures behavior may be informative context without being identical to spot/CFD behavior.
- evidence_refs: GOLD_MICROSTRUCTURE.md, DATA_CAPABILITY_MAP.md.
- claim_status: CORROBORATED as a data-domain definition.
- evaluation_tests: field-availability and venue-attribution tests.
- decision_safety: venue-scoped only.

## G003 — Cross-Venue Observation
- type: data_domain_relation
- title: Cross-Venue Observation
- definition: A comparison between distinct gold data domains.
- operational_definition: Align timestamps causally, preserve source identity and record disagreement rather than silently merging observations.
- observable_inputs: observations from at least two identified domains, timestamps.
- data_requirements: source identity and time alignment.
- applicable_conditions: cross-venue context.
- weak_conditions: latency mismatch, different instruments, missing timestamps.
- failure_modes: constructing one synthetic order-flow series from distinct venues.
- competing_interpretations: disagreement may reflect instrument, venue, latency or market-structure differences.
- evidence_refs: DATA_QUALITY_CONTRACT.md.
- claim_status: CORROBORATED as a data-discipline principle.
- evaluation_tests: timestamp alignment and disagreement-preservation cases.
- decision_safety: comparison only; no universal market inference.

## G004 — Tick Activity Proxy
- type: proxy
- title: Tick Activity Proxy
- definition: Broker/feed-specific activity count.
- operational_definition: Record source/feed, interval and activity measurement type; always label the value as a proxy.
- observable_inputs: tick/activity count, source, timestamp.
- data_requirements: broker/feed tick stream.
- applicable_conditions: local activity context.
- weak_conditions: feed-specific aggregation and cross-broker comparison.
- failure_modes: labeling tick activity as centralized traded volume.
- competing_interpretations: activity can reflect quote generation rather than executed volume.
- evidence_refs: GOLD_MICROSTRUCTURE.md, DATA_CAPABILITY_MAP.md, FEATURE_DEFINITIONS_V1.
- claim_status: CORROBORATED as a proxy definition.
- evaluation_tests: metadata preservation and broker-change sensitivity.
- decision_safety: cannot establish centralized volume, liquidity or intent.

## G005 — Event-State Separation
- type: event_context
- title: Event-State Separation
- definition: Pre-event, event-window, immediate post-event and later repricing are distinct analytical states.
- operational_definition: Assign state using versioned event timestamps/windows and only information available at each timestamp; never use the future event outcome for pre-event classification.
- observable_inputs: event timestamp, current timestamp, event-window metadata, price/volatility observations.
- data_requirements: reliable event calendar and timestamp integrity.
- applicable_conditions: event-sensitive market analysis.
- weak_conditions: unscheduled events, stale calendars, ambiguous release times.
- failure_modes: future-event leakage and attributing all post-event movement to the event.
- competing_interpretations: event effect may coexist with ordinary structure, session transition or liquidity changes.
- evidence_refs: EVENT_SESSION_MODEL.md, FEATURE_DEFINITIONS_V1.
- claim_status: CORROBORATED as an evidence-separation principle.
- evaluation_tests: pre/post boundary and leakage cases.
- decision_safety: event-state metadata constrains interpretation; it does not predict event direction.
