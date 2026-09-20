# Gold Data-Domain Objects V1

## G001 — Broker XAUUSD Feed
Represents the broker-specific spot/CFD price and execution environment.
Use: execution facts and broker-local price observations.
Cannot represent: the complete global gold market or centralized order flow.

## G002 — CME/COMEX Gold Futures
Represents an exchange-traded gold futures venue with centralized transaction and order-book data when such feeds are available.
Use: venue-specific volume/order-flow analysis.
Cannot represent: every spot/CFD participant.

## G003 — Cross-Venue Observation
A comparison between gold data domains.
Rule: preserve source identity, timestamp alignment and disagreement.
Cannot: silently merge futures flow with broker CFD flow.

## G004 — Tick Activity Proxy
Broker/feed-specific activity count.
Use: activity context only.
Cannot: be labeled as centralized traded volume.

## G005 — Event-State Separation
Pre-event, event-window, immediate post-event and later repricing are distinct analytical states.
Rule: never use the future event outcome in a pre-event decision.
