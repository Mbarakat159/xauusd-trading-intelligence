# Regime Contract V1

## Purpose
Define a machine-readable conceptual contract for market state without prescribing an entry strategy.

## State dimensions
Each dimension returns:
- state distribution or calibrated score;
- supporting observations;
- conflicting observations;
- missing evidence;
- timestamp/cutoff;
- confidence dimensions;
- transition status.

### Directional structure
Possible states: directional-up, directional-down, non-directional, transition, unknown.

### Volatility
Possible states: compressed, normal, expanded, shock, transition, unknown.

### Liquidity/activity
Possible states: thin, normal, active, stressed, unknown.

### Auction/location
Possible states: balanced, accepted-above, accepted-below, rejecting, migrating, unknown.

### Event state
Possible states: ordinary, pre-event, event-window, post-event-repricing, unresolved, unknown.

### Structural state
Possible states: continuation, consolidation, breakout-transition, reversal-transition, structural-conflict, unknown.

## Important constraint
These labels are descriptive state representations. They are not direct buy/sell signals.

## Calibration
If probabilities are emitted, calibration must be evaluated separately from directional trading outcomes. A high probability means the classifier is expressing calibrated state uncertainty, not a probability of trade profit.

## Transition handling
A transition is a first-class state. The system must not force the market into the previous regime until a new regime is confirmed.

## Output
The regime component returns state, evidence, conflicts, missing_data, transition, calibration_metadata and version.
