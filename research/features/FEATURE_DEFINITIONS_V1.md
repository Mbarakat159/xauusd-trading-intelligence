# Deterministic Feature Definitions V1

## Purpose
Canonical measurement contracts referenced by knowledge objects. These definitions specify what a feature means, what information it may use, and which parameters must be versioned. They do not prescribe trading thresholds.

## Global contract
Every feature must be computed causally at a declared decision timestamp. Parameters, lookback windows, thresholds, confirmation rules, calendars and transformations are versioned inputs. A missing or invalid required input returns UNKNOWN/quality flags rather than an invented value.

## F001 — OHLC Geometry
Definition: basic candle consistency.
Inputs: open, high, low, close.
Invariant: high >= max(open, close) and low <= min(open, close), with high >= low.
Failure: INVALID when violated.

## F002 — Returns
Definition: price change relative to the immediately preceding valid close.
Inputs: current close, previous valid close.
Rule: no return when previous close is unavailable or invalid.

## F003 — True Range
Definition: current-period range using current high/low and the immediately preceding valid close.
Inputs: current OHLC, previous valid close.
Rule: causal only; no future observations.

## F004 — Realized Volatility
Definition: dispersion of returns over a declared causal lookback.
Inputs: causal return series, versioned lookback/estimator.
Rule: all observations must be available by the cutoff.

## F005 — Volatility Baseline
Definition: a versioned reference distribution or statistic against which current variability is compared.
Inputs: causal volatility observations, baseline window/estimator.
Rule: baseline parameters are fixed before evaluation; outcome-dependent threshold selection is prohibited.

## F006 — Range Position
Definition: current price location within a declared causal high/low reference interval.
Inputs: price, reference high/low.
Rule: UNKNOWN when the interval is undefined or high equals low.

## F007 — Confirmed Swing
Definition: a swing high/low that becomes usable only after its declared confirmation condition occurs.
Inputs: causal OHLC, timeframe, versioned swing parameters.
Rule: confirmation timestamp is the earliest usable timestamp; later candles cannot retroactively make an earlier decision aware of the swing.

## F008 — Structural Reference
Definition: a price level derived from a previously confirmed structural observation.
Inputs: confirmed swings/levels, causal cutoff.
Rule: level selection must be deterministic or explicitly versioned; future-selected levels are prohibited.

## F009 — Structural Break
Definition: first timestamp at which a declared break criterion becomes true against a previously available structural reference.
Inputs: F008, causal OHLC/quotes, versioned break criterion.
Rule: wick/body and confirmation semantics must be declared in the feature version.

## F010 — Structural Distance
Definition: causal distance between current price and a previously available structural/reference level.
Inputs: price, F008.
Rule: no future-selected reference.

## F011 — Spread
Definition: same-source bid/ask difference at a timestamp.
Inputs: bid, ask, source.
Rule: never reconstruct spread from OHLC; invalid/inconsistent quotes propagate quality failure.

## F012 — Activity / Tick Proxy
Definition: broker/feed-specific count of tick or activity events over a declared interval.
Inputs: source/feed, interval, activity count.
Rule: labeled proxy; never represented as centralized transaction volume.

## F013 — Volume Provenance
Definition: metadata classifying whether volume is exchange-reported trades, another defined venue measurement, broker activity, or UNKNOWN.
Required metadata: venue, instrument, source, timestamp, aggregation interval, measurement type.

## F014 — Event Distance
Definition: causal temporal distance from the current timestamp to a scheduled event timestamp.
Inputs: authoritative event timestamp, timezone, current timestamp.
Rule: event outcome/publication result is never an input to pre-event classification.

## F015 — Session State
Definition: timestamp classification under a versioned venue/session calendar and timezone.
Inputs: timestamp, calendar version, timezone.
Rule: DST, holidays and calendar changes are explicit; session label has no directional meaning.

## F016 — MTF Synchronization
Definition: causal alignment of observations across declared timeframe sampling intervals.
Inputs: bar-close timestamps, timeframe definitions, source identity.
Rule: incomplete future bars cannot be used; each observation retains its own timestamp and confirmation delay.

## F017 — Event Window
Definition: versioned classification of pre-event, event-window, post-event or ordinary state from event metadata.
Inputs: F014 plus versioned window parameters.
Rule: window parameters are declared before evaluation and do not depend on observed price outcome.

## F018 — Proxy Capability
Definition: mapping between a claim and the minimum data fields required to support that claim.
Inputs: claim type, venue, available fields.
Outputs: SUFFICIENT, PARTIAL, or UNKNOWN.
Rule: proxies may support narrower claims only when explicitly relabeled; silent substitution is prohibited.

## Feature dependency rule
Knowledge objects must reference these feature contracts when their operational definitions depend on measurements. A feature contract defines measurement semantics, not a universal trading threshold.

## Promotion requirements
A feature is not promoted merely because values look plausible. It requires formula/boundary tests, causality tests, missing-data tests, timestamp tests, parameter/version records and documented limitations.
