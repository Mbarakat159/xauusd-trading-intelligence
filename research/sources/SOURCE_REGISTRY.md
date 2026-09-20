# Source Registry

Living research registry for the independent XAUUSD intelligence layer.

## High-priority sources

| Source | Class | Coverage | Reusable finding | Limitation |
|---|---|---|---|---|
| TauricResearch/TradingAgents | C | multi-agent trading architecture | analyst separation, debate, risk/portfolio separation, provenance | architecture does not prove alpha |
| yebof/quant-agent | C | quant-agent architecture | deterministic risk filters, structured risk layer, persistent memory | implementation choices are not universal truth |
| gentodev/ai-trading-agent | C | technical/sentiment/risk agents | multi-timeframe inputs and role separation | implementation dependent |
| JesstLe/quant-agent | C | research/strategy/risk/execution | explicit role separation | no proof of durable edge |
| Public Fable-related repositories | C/E | agentic behavior | outcome orientation, evidence before state change, verification, recovery | leaked prompt material must not be copied wholesale |
| SSRN: Chaboud et al., Rise of the Machines | A/B | FX algorithmic trading | algorithmic/human order flow, macro-release behavior and liquidity deserve explicit treatment | historical FX sample, not XAUUSD-specific |
| SSRN: Yang, Lin & Huang, 2026 systematic review | A/B | AI, algorithms, microstructure | liquidity, price discovery, fragility and correlated behavior are central dimensions | broad review, not a trading recipe |
| SSRN: Yang, Faster Is Not Calmer, 2026 | A/B | agentic AI and volatility | reaction-time compression can affect event-time volatility and temporary displacement | theoretical model |
| SSRN: regime-adaptive trading framework | B | regimes, trend/mean reversion, risk | regime classification should be first-class research | documented limitations |
| SSRN: risk-sensitive RL under regime shifts | B | risk under non-stationarity | downside constraints and regime shifts deserve explicit treatment | controlled research setting |
| SSRN: position-sizing evaluation framework | B | sizing/frictions/drawdown | sizing evaluation must include costs, drawdown and ruin dynamics | methodology paper, not XAUUSD validation |

## Source rules

1. Preserve the original URL/repository and review date.
2. Record supported claims, not inferred claims.
3. Separate conceptual usefulness from empirical evidence.
4. Record instrument, market, timeframe, sample period and assumptions.
5. Preserve contradictions.
6. GitHub implementation is not proof of profitability.
7. A backtest is not universal evidence for live XAUUSD.
8. Practitioner frameworks remain hypotheses until independently supported.
9. Do not reproduce proprietary or leaked system prompts; extract general principles only.
10. Prefer primary research and official documentation when claims conflict.

## Next research priorities

- XAUUSD/gold-specific microstructure and liquidity.
- Event-window behavior.
- Regime identification under non-stationarity.
- Order-flow proxies when true order-book data are unavailable.
- Position sizing under friction and drawdown.
- Agentic verification and recovery.
