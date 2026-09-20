# Core Knowledge Objects V1

These are foundational concepts, not a trading strategy.

## K001 — Market State
Definition: a description of current observable market conditions across structure, volatility, liquidity/activity, auction/location and event state.
Operational use: organize observations before selecting analytical methods.
Cannot establish: future direction or profitability.
Status: CORROBORATED conceptually; operational implementation pending evaluation.

## K002 — Trend
Definition: persistent directional structural behavior under a declared swing/structure definition.
Operational requirement: exact swing definition and confirmation timing.
Failure mode: labeling a short impulse as a durable trend.
Status: CLAIMED until the operational definition is tested.

## K003 — Range/Balance
Definition: a condition in which price remains bounded around an evolving accepted area under a declared measurement rule.
Cannot establish: that the next break will occur in either direction.
Failure mode: treating every pause as balance.
Status: CLAIMED.

## K004 — Volatility Regime
Definition: the current scale and stability of price variability relative to a declared reference.
Operational inputs: true range/returns and a causal window.
Cannot establish: direction.
Status: CORROBORATED conceptually; exact detector pending.

## K005 — Liquidity Proxy
Definition: an observable variable that may relate to trading activity or execution conditions but is not itself proof of hidden liquidity.
Gold-specific warning: broker tick activity is not centralized traded volume.
Status: CORROBORATED under data-capability constraints.

## K006 — Structural Break
Definition: price crossing a previously confirmed structural reference under a declared break rule.
Cannot establish: continuation after the break.
Failure mode: using future-confirmed levels.
Status: CLAIMED pending feature tests.

## K007 — Rejection
Definition: observable failure to maintain price beyond a declared reference, measured from actual price behavior.
Alternative interpretation: rejection can reflect temporary liquidity/volatility rather than durable reversal.
Status: CLAIMED.

## K008 — Displacement
Definition: unusually large directional price movement relative to a declared causal volatility baseline.
Cannot establish: institutional intent.
Status: CLAIMED pending threshold evaluation.

## K009 — MTF Context
Definition: a relationship among observations at different timeframes where each timeframe has an analytical role.
Anti-pattern: treating timeframe count as voting.
Status: CORROBORATED conceptually; implementation pending.

## K010 — Invalidation
Definition: a predeclared observable condition that materially contradicts a hypothesis.
Requirement: defined before outcome is known.
Status: CORROBORATED as a reasoning principle.

## K011 — Stop Efficiency
Definition: relationship between stop distance, thesis invalidation, volatility/noise and execution conditions.
Cannot establish: whether the thesis itself will succeed.
Status: CORROBORATED conceptually; quantitative evaluation pending.

## K012 — Evidence Conflict
Definition: material disagreement between observations, methods, sources or timeframes relevant to the same hypothesis.
Required behavior: preserve the conflict; do not average it away.
Status: CORROBORATED as evidence-discipline principle.
