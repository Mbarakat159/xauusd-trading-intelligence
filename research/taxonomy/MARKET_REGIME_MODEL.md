# Market Regime Model

The regime model is a latent-state hypothesis layer. It must remain probabilistic and revisable.

## Core state dimensions

### Directional state
- directional trend
- weak trend
- range/balance
- transition
- ambiguous

### Volatility state
- compressed
- normal
- expanding
- extreme/shock

### Liquidity state
- normal
- thin
- improving
- stressed
- event-distorted

### Auction state
- acceptance/value formation
- rejection
- balance
- imbalance/displacement
- failed auction

### Event state
- normal
- pre-event
- event window
- post-event repricing
- unresolved event risk

### Structural state
- continuation
- pullback
- breakout attempt
- failed breakout
- reversal attempt
- transition between states

## Why this is not a single label

A market can simultaneously be structurally bullish, volatility-expanding, near an important prior extreme, in an event window, and showing contradictory short-term order flow.

Therefore the intelligence layer should represent a state vector rather than force one label.

## Evidence hierarchy

Prefer observable evidence:
1. direct market data;
2. derived measurements;
3. cross-timeframe structural relationships;
4. contextual/macro information;
5. interpretive framework labels.

Framework labels such as accumulation, liquidity grab, or smart-money move should remain hypotheses unless observable evidence supports them.

## Regime transition triggers

Monitor:
- break and acceptance beyond prior structure;
- repeated failure at a boundary;
- volatility expansion/contraction;
- abnormal range/volume behavior;
- changes around scheduled events;
- loss of directional persistence;
- liquidity/execution deterioration.

## Required output

The future implementation should expose:
- current state vector;
- supporting observations;
- conflicting observations;
- uncertainty;
- recent state transitions;
- conditions that would invalidate the current regime hypothesis.

No trade decision should depend on the regime label alone.
