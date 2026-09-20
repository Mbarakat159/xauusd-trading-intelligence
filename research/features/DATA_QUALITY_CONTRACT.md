# Data Quality Contract

No reasoning layer may silently compensate for bad market data.

## Required metadata
Every observation must carry:
- source/feed;
- venue when known;
- instrument;
- timestamp and timezone;
- timeframe;
- arrival/collection timestamp;
- freshness;
- sequence/order information where applicable;
- transformation/version;
- missing-data flags.

## Quality states
VALID, STALE, MISSING, CONFLICTING, INVALID, UNKNOWN.

UNKNOWN is preferred to an invented value.

## Hard failures
The reasoning layer must not treat data as current when:
- timestamp is older than the declared freshness budget;
- required fields are missing;
- timestamps are non-monotonic without an explicit correction record;
- bid/ask are inconsistent;
- OHLC violates basic bounds;
- event timestamps are ambiguous;
- venue/source identity is missing for venue-specific claims.

## Cross-source disagreement
Do not average away disagreement. Preserve source-specific observations and expose the conflict to reasoning.

## Time integrity
All event/session calculations use explicit timezone rules. DST and calendar changes are versioned.

## Gold-specific integrity
XAUUSD broker prices, London/spot references and CME futures observations are distinct data domains. They may be compared, but never silently merged into one order-flow series.

## Recovery
On data failure:
1. detect;
2. classify;
3. attempt bounded recovery if configured;
4. revalidate;
5. otherwise degrade to a safe action.

## Promotion gate
A component that depends on data quality cannot be promoted until stale, missing, conflicting and delayed-data cases are tested.
