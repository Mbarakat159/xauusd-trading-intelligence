# Trading Methodology Matrix

This is a research map, not an entry strategy.

The intelligence layer must choose analytical tools according to observed market state and available evidence rather than activating a fixed indicator stack.

| Method family | Primary question | Useful observations | Potential regimes | Failure modes / cautions |
|---|---|---|---|---|
| Market structure | What state is price structurally in? | swings, breaks, acceptance/rejection, compression/expansion | all | swing definitions can be subjective and timeframe-dependent |
| Price action | What is price communicating at a location? | rejection, displacement, continuation, failed break | all | isolated candle patterns are weak without context |
| Support/resistance | Where has price previously reacted? | prior highs/lows, ranges, pivots | range, transition, trend pullbacks | levels are zones, not guaranteed barriers |
| Supply/demand | Where did imbalance/repricing originate? | impulsive departures, bases, retests | trend/transition | definitions vary materially across schools |
| Wyckoff | Is accumulation/distribution and effort-vs-result plausible? | range behavior, tests, springs/upthrusts, volume | range/transition | interpretation can become narrative-heavy |
| Auction/market profile | Where did the market accept/reject value? | value area, POC, HVN/LVN, acceptance | range/transition | requires appropriate volume/data construction |
| Liquidity analysis | Where may orders/liquidity cluster and what happened after a sweep? | equal highs/lows, prior extremes, sweep + response | all | liquidity terminology is often used without observable evidence |
| Order flow | What is happening in aggressive/passive flow? | delta, imbalance, footprint, DOM, tape | intraday/event | data quality and venue coverage are critical |
| VWAP | Where is volume-weighted reference value? | VWAP, deviations, acceptance | intraday/trend/range | session definition matters |
| Volume | Is participation expanding or contracting? | relative volume, climax, absorption proxies | all | spot FX/CFD volume may be tick/venue-specific |
| Classical momentum | Is directional pressure changing? | RSI, stochastic, MACD, Williams | trend/transition | lag, redundancy, false signals in ranges |
| Trend strength | Is directional movement meaningful? | ADX and directional components | trend/transition | high values can persist after late entries |
| Volatility | How large/fast are expected moves? | ATR, realized range, Bollinger width, volatility regime | all | volatility is not direction |
| Statistical/quantitative | Is the observed behavior unusual or persistent? | distributions, autocorrelation, z-scores, correlations, regime models | all | non-stationarity and multiple testing |
| Mean reversion | Is deviation likely to contract? | distance from reference/value, volatility-normalized deviation | range/low trend | dangerous during persistent trends |
| Trend following | Is persistence strong enough to follow? | structure + momentum + volatility expansion | trend | whipsaw during transition/range |
| Breakout | Is price leaving a prior balance with acceptance? | compression, range boundary, displacement, retest | transition/expansion | false breaks |
| Reversal | Is prior direction failing? | exhaustion, failed break, structural shift | transition | catching falling/rising markets too early |
| Fibonacci | Are retracement/extension zones useful references? | measured retracements/extensions | trend/transition | high degrees of freedom; level selection can be subjective |
| Harmonics | Does a geometric pattern exist? | ratio-based swing geometry | transition | pattern mining and hindsight risk |
| Elliott | What wave interpretation is plausible? | nested swings | all | multiple valid counts; high subjectivity |
| Macro/fundamental | What external information changes valuation/risk? | rates, USD, inflation, central-bank signals, employment | event/regime | timing and transmission can differ from narrative |
| Session/microstructure | What changes with time-of-day? | liquidity, spreads, overlap, opens/closes | intraday | broker/venue specific |
| Multi-timeframe reasoning | How do context, setup, trigger and invalidation relate? | nested structure and conflicting horizons | all | independent timeframe votes can create false confidence |

## Core design rule

No method family receives permanent priority.

The future intelligence engine should:
1. identify the current market state;
2. identify which observations are actually available;
3. select relevant analytical families;
4. generate competing hypotheses;
5. search for disconfirming evidence;
6. define invalidation;
7. assess execution and risk;
8. choose among trade, reduced-risk action, or wait only after evidence synthesis.

A method being useful in a regime means it is worth investigating under that regime, not that it is guaranteed to work.
