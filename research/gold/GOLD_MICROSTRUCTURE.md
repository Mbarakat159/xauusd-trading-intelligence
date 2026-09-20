# Gold / XAUUSD Microstructure Research

## Key research finding

Gold price discovery is distributed across London spot and New York futures, but the relative contribution varies intraday, across years, with liquidity, daylight hours and macro announcements. Research using 17 years of intraday data found a larger average price-discovery contribution from New York futures despite lower reported volume than London spot. This means the intelligence layer must not treat a broker's XAUUSD CFD feed as the complete market. Source: Hauptfleisch, Putnins & Lucey, *Who Sets the Price of Gold? London or New York?* (SSRN 2606587).

## Consequences for the agent

1. XAUUSD broker quotes are an execution venue/feed, not the entire gold market.
2. CME/COMEX gold futures can be an important reference for price discovery and order-flow research.
3. Session and macro-event context can change where information is incorporated.
4. Volume/order-flow observations must always identify the venue.
5. A futures footprint cannot be blindly described as the order flow of the entire XAUUSD market.

## Session dimension

Research on gold and platinum futures finds meaningful intraday differences between Tokyo and New York sessions, including differences in liquidity and informed-trading activity.

Therefore session should be represented as market context, not merely a trading-hours filter.

## Data model implication

The future knowledge interface should distinguish:

- broker/CFD quote;
- spot/reference market;
- futures market;
- exchange-traded volume;
- tick volume;
- order-book data;
- derived cross-market relationships.

## Important limitation

These studies describe market structure and price discovery. They do not prove a particular trading strategy.

## Research status

Strong conceptual evidence. XAUUSD execution-specific behavior still requires broker/venue research.
