# Gold Event and Session Model

## Context dimensions

The future market state should include:
- session;
- session overlap;
- scheduled macro event proximity;
- event severity;
- pre-event positioning/volatility;
- event-window execution conditions;
- post-event repricing;
- unresolved macro information.

## Research basis

Gold research shows that price discovery and market microstructure vary across London/New York and around macroeconomic announcements. Therefore session and event state should influence interpretation and execution assumptions, not simply produce BUY/SELL filters.

## Event reasoning

The system should distinguish:
1. before the event: uncertainty and execution risk can increase;
2. during the event: spreads, volatility and price discovery can change abruptly;
3. immediately after: initial move may continue, reverse or consolidate;
4. later: the market may establish a new accepted range.

The correct response is observation and evidence gathering, not an assumed directional rule.

## Required event audit

For each event-sensitive decision store:
- event name/category;
- scheduled time;
- distance from event;
- relevant market variables;
- observed pre-event state;
- observed event response;
- execution conditions;
- post-event state;
- unresolved uncertainty.
