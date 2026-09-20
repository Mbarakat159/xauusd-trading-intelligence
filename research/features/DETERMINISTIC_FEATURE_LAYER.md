# Deterministic Feature Layer

## Role
Convert raw market data into auditable E0/E1 observations before any LLM interpretation.

RAW DATA -> VALIDATION -> DETERMINISTIC FEATURES -> E0/E1 -> REASONING

## Design rules
- No LLM-generated measurements.
- No future-data access.
- Every feature has an exact mathematical/algorithmic definition.
- Every output carries source timestamp, timeframe, venue/feed and freshness.
- Missing/invalid inputs produce explicit UNKNOWN, never invented values.
- Features are versioned; changing a definition creates a new feature version.

## Initial feature families
### Price/structure
OHLC, returns, candle geometry, swing candidates, confirmed swings, range boundaries, displacement, gap-like discontinuity, breakout/retest state.

### Volatility
ATR, realized volatility, true-range statistics, volatility expansion/contraction.

### Location
Distance to confirmed structural levels, session extremes, VWAP where data is available, recent range position.

### Market activity
Spread, tick-volume/activity proxies, session/overlap state.

### Cross-market/event context
Only when data is actually available: DXY, rates/yields, futures reference, calendar-event distance and event severity.

## Confirmation policy
A feature that requires future confirmation (for example a confirmed swing) must carry a confirmation delay. The system must not pretend it was known at the earlier timestamp.

## Gold-specific data rule
Broker XAUUSD/CFD data is not equivalent to centralized futures order flow. Venue-specific order-book/volume observations must be labeled as such.

## Testing
Each feature requires:
- formula/algorithm;
- edge cases;
- causality test;
- missing-data test;
- timezone/session test;
- numerical tolerance;
- unit tests before use by reasoning.

## Promotion gate
No feature enters the reasoning layer merely because it is familiar or useful in a trading framework. It must be precisely defined, testable and provenance-aware.
