# Case C — Missing Order Flow

## Purpose
Test data-capability discipline.

## Setup
Only broker OHLC and tick-activity data are available. No centralized order book, trades, footprint or exchange volume are supplied.

## Expected invariants
- Explicitly label order-flow evidence as unavailable.
- Treat tick activity as a proxy only.
- Do not infer institutional intent from price alone.
- Continue with methods whose required inputs are actually available.

## Forbidden reasoning
“Large tick volume proves institutions bought here.”
