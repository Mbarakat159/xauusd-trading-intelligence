# Deterministic Feature Definitions V1

This is a specification, not an executable trading strategy.

## 1. Candle geometry
Given OHLC:
- range = high - low
- body = abs(close - open)
- upper_wick = high - max(open, close)
- lower_wick = min(open, close) - low
Undefined bars are rejected.

## 2. True Range
TR(t) = max(high-low, abs(high-prev_close), abs(low-prev_close)).
The previous close must belong to the same validated series.

## 3. ATR
ATR is a specified moving average of TR over a declared period. The exact smoothing method and period are configuration, not hidden defaults. The output carries its parameter version.

## 4. Returns
Simple return = close(t)/close(t-1)-1. Log return = ln(close(t)/close(t-1)).
No return is emitted when the previous observation is missing or invalid.

## 5. Realized volatility
For a declared window, compute the standard deviation of log returns using only observations at or before the decision timestamp. Annualization, if used, is metadata and must not be assumed.

## 6. Range position
For a declared lookback [L,H], position = (price-L)/(H-L). If H=L, output UNKNOWN.

## 7. Confirmed swing
A swing high/low requires a declared left/right confirmation rule. A swing becomes observable only at the first timestamp when the confirmation condition is satisfied. Earlier timestamps must not contain the confirmed label.

## 8. Structural level distance
Distance is measured from the current reference price to a confirmed level. The level's creation/confirmation timestamp is retained. Levels are not allowed to use future-confirmed pivots.

## 9. Displacement
Displacement is not a vague visual label. V1 defines it as a bar/range movement exceeding a declared robust threshold relative to recent true-range statistics, with direction and timestamp recorded. Thresholds are parameters and require separate evaluation.

## 10. Break condition
A break is a relation between current price and a previously confirmed structural level, with a declared close/touch requirement. The event timestamp is when the condition becomes observable, not when a later retest occurs.

## 11. Spread
Spread = ask - bid when both are available from the same feed and timestamp. If only OHLC exists, spread is UNKNOWN, never inferred.

## 12. Activity proxy
Tick volume/activity is labeled as feed-specific activity. It must never be named traded volume unless the source is a centralized transaction-volume feed.

## 13. Session state
Session labels are deterministic mappings from timestamp + declared timezone/calendar. DST changes and holidays must be handled explicitly.

## 14. Event distance
Event distance is time between decision timestamp and a known calendar event timestamp. Event severity and revision status are separate fields. The event outcome must not be visible before publication.

## 15. Data freshness
freshness = decision_timestamp - latest_valid_source_timestamp.
A maximum allowed age is a risk/data-quality policy, not a market feature.

## Feature contract
Every feature record must include:
feature_id, version, source, venue/feed, timeframe, observation_timestamp, calculation_timestamp, parameters, value, status, quality_flags.

## Non-negotiable causality rule
A feature is invalid for decision use if any input was only knowable after the decision timestamp.

## Versioning
Changing a formula, confirmation rule, parameter default, timezone convention or missing-data behavior creates a new feature version.
