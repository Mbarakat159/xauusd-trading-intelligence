# XAUUSD Data Capability Map

The agent must know what it can actually observe before making a market claim.

| Data type | What it can support | What it cannot prove by itself |
|---|---|---|
| OHLC | structure, ranges, break/rejection, volatility, price action | true order-flow intent |
| Tick volume | activity proxy within the feed | centralized traded volume |
| Broker spread | execution environment | global liquidity |
| Futures volume | exchange participation | total global gold volume |
| Futures footprint/delta | aggressive-flow observations on that venue | entire spot/CFD flow |
| DOM / Level 2 | displayed liquidity on a venue | hidden liquidity or global book |
| Tape / time & sales | executed trades on a venue | all global transactions |
| VWAP | volume-weighted reference for a specified dataset/session | universal fair value |
| News/calendar | scheduled event context | exact market reaction |
| DXY/rates/yields | cross-market context | deterministic gold direction |
| Positioning data | participant-position context | exact current order placement |
| Broker account state | executable risk/exposure facts | market-wide conditions |

## Mandatory provenance

Every observation should carry:
- source venue;
- timestamp;
- timeframe;
- data type;
- transformation;
- freshness;
- missing-data flags.

## No-data rule

If the agent does not have real order-book or transaction-flow data, it must say that it is using a proxy rather than fabricate an order-flow conclusion.

## Cross-market rule

If futures, spot/CFD, DXY or rates disagree, preserve the disagreement as evidence rather than forcing a single narrative.
