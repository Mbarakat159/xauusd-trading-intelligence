# Core Knowledge Objects V1

These are foundational concepts, not a trading strategy. Measurement semantics use `research/features/FEATURE_DEFINITIONS_V1.md` where applicable.

## K001 — Market State
- type: state
- title: Market State
- definition: A description of current observable market conditions across structure, volatility, liquidity/activity, auction/location and event state.
- operational_definition: Assemble only timestamp-causal observations available at the decision cutoff; preserve missing/conflicting dimensions explicitly.
- observable_inputs: structure, volatility, liquidity/activity, auction/location, event state.
- data_requirements: validated observations with provenance and timestamp.
- applicable_conditions: initial state description before method selection.
- weak_conditions: missing dimensions, conflicting sources, stale data.
- failure_modes: filling unknown state with inference; collapsing conflicts into one label.
- competing_interpretations: multiple state dimensions may disagree without one being invalid.
- evidence_refs: REGIME_CONTRACT_V1, DATA_QUALITY_CONTRACT.
- claim_status: CORROBORATED conceptually; operational implementation pending evaluation.
- evaluation_tests: missing-data, conflict-preservation and causality cases.
- decision_safety: descriptive state only.

## K002 — Trend
- type: concept
- title: Trend
- definition: Persistent directional structural behavior under a declared swing/structure definition.
- operational_definition: Use confirmed swings available at the decision cutoff and a versioned structural classification; do not infer persistence from future movement.
- observable_inputs: confirmed swings, timeframe, structural state.
- data_requirements: F007 Confirmed Swing and causal OHLC.
- applicable_conditions: directional structure assessment.
- weak_conditions: transitions, compressed ranges, insufficient confirmed swings.
- failure_modes: labeling a short impulse as durable trend; future-confirmed pivots.
- competing_interpretations: local directional movement may be noise, retracement or transition.
- evidence_refs: FEATURE_DEFINITIONS_V1, K013.
- claim_status: CLAIMED until operational definition is tested.
- evaluation_tests: causality, confirmation delay, transition cases.
- decision_safety: contextual evidence only.

## K003 — Range / Balance
- type: concept
- title: Range / Balance
- definition: A condition in which price remains bounded around an evolving accepted area under a declared measurement rule.
- operational_definition: Use the versioned balance/location and persistence criteria; return UNKNOWN when required causal criteria are unavailable.
- observable_inputs: price path, reference area, range position, persistence/rotation features.
- data_requirements: causal intraday data and declared criteria.
- applicable_conditions: non-directional and transitional states.
- weak_conditions: event windows, rapidly migrating markets, unstable reference areas.
- failure_modes: treating every pause as balance.
- competing_interpretations: pause within trend, compression, accumulation/distribution hypothesis.
- evidence_refs: K019, FEATURE_DEFINITIONS_V1.
- claim_status: CLAIMED.
- evaluation_tests: range/breakout transition cases.
- decision_safety: descriptive state.

## K004 — Volatility Regime
- type: state
- title: Volatility Regime
- definition: The current scale and stability of price variability relative to a declared reference.
- operational_definition: Use causal realized-volatility/range measurements and a versioned baseline; state is UNKNOWN when the baseline cannot be constructed.
- observable_inputs: returns, true range, ATR/realized volatility, baseline.
- data_requirements: F002-F005 with sufficient causal history.
- applicable_conditions: regime and execution assessment.
- weak_conditions: insufficient sample, feed discontinuity, event shock without event metadata.
- failure_modes: outcome-dependent baseline selection; confusing event shock with ordinary regime.
- competing_interpretations: expansion may be ordinary regime change, event shock or data anomaly.
- evidence_refs: FEATURE_DEFINITIONS_V1, REGIME_CONTRACT_V1.
- claim_status: CORROBORATED conceptually; exact detector pending evaluation.
- evaluation_tests: boundary, causality and transition tests.
- decision_safety: does not establish direction.

## K005 — Liquidity Proxy
- type: proxy
- title: Liquidity Proxy
- definition: An observable variable that may relate to trading activity or execution conditions but is not proof of hidden liquidity.
- operational_definition: Name the proxy, source/venue, transformation and known bias; retain proxy provenance in downstream records.
- observable_inputs: spread, tick activity, quote updates, realized volatility, depth where available.
- data_requirements: explicit source/venue provenance.
- applicable_conditions: when direct liquidity data are unavailable.
- weak_conditions: cross-venue inference and broker-only feeds.
- failure_modes: proxy treated as ground truth.
- competing_interpretations: activity can reflect news or quoting behavior rather than executable liquidity.
- evidence_refs: G004, K021, FEATURE_DEFINITIONS_V1.
- claim_status: CORROBORATED under data-capability constraints.
- evaluation_tests: proxy-vs-direct-data tests where available.
- decision_safety: proxy only; never direct liquidity proof.

## K006 — Structural Break
- type: concept
- title: Structural Break
- definition: Price crossing a previously confirmed structural reference under a declared break rule.
- operational_definition: Use F008 Structural Reference and F009 Structural Break with a versioned break criterion available before evaluation.
- observable_inputs: confirmed structural level, OHLC/quote data.
- data_requirements: causal price data and confirmed reference.
- applicable_conditions: structural transition analysis.
- weak_conditions: spread expansion, event windows, thin liquidity, ambiguous levels.
- failure_modes: future-selected levels, wick/body ambiguity, false-break classification.
- competing_interpretations: continuation, liquidity test, rejection, structural transition.
- evidence_refs: FEATURE_DEFINITIONS_V1, K015.
- claim_status: CLAIMED pending feature tests.
- evaluation_tests: causality, event-risk and disconfirmation cases.
- decision_safety: context evidence requiring confirmation.

## K007 — Rejection
- type: concept
- title: Rejection
- definition: Observable failure to maintain price beyond a declared reference, measured from actual price behavior.
- operational_definition: Use a versioned reference, observation horizon and persistence/return criterion; classify only from data available at the cutoff.
- observable_inputs: price path, reference level, observation horizon.
- data_requirements: causal price/quote sequence.
- applicable_conditions: interaction with structural/auction references.
- weak_conditions: event shocks, sparse data, ambiguous reference.
- failure_modes: naming rejection only after a later directional outcome.
- competing_interpretations: temporary volatility, failed breakout, ordinary rotation.
- evidence_refs: K017, FEATURE_DEFINITIONS_V1.
- claim_status: CLAIMED.
- evaluation_tests: predeclared horizon and adversarial rejection cases.
- decision_safety: descriptive/hypothesis evidence only.

## K008 — Displacement
- type: concept
- title: Displacement
- definition: Unusually large directional price movement relative to a declared causal volatility baseline.
- operational_definition: Use F005 Volatility Baseline and a versioned threshold fixed before evaluation.
- observable_inputs: returns/range/ATR, volatility baseline.
- data_requirements: sufficient causal OHLC.
- applicable_conditions: expansion and structural-event detection.
- weak_conditions: event shocks and feed anomalies unless explicitly separated.
- failure_modes: volatility-regime confusion, threshold drift, institutional-intent inference.
- competing_interpretations: genuine repricing, event shock, liquidity vacuum.
- evidence_refs: FEATURE_DEFINITIONS_V1, K018.
- claim_status: CLAIMED pending threshold evaluation.
- evaluation_tests: threshold invariants, event-risk separation.
- decision_safety: observation only.

## K009 — MTF Context
- type: contextual_reasoning
- title: MTF Context
- definition: A relationship among observations at different timeframes where each timeframe has an analytical role.
- operational_definition: Preserve timeframe identity, causal synchronization and role metadata; do not aggregate timeframes by vote.
- observable_inputs: timeframe states, timestamps, roles.
- data_requirements: F016 MTF Synchronization.
- applicable_conditions: multi-timeframe analysis.
- weak_conditions: unsynchronized data, missing bars, unresolved transitions.
- failure_modes: timeframe majority voting; universal agreement requirement.
- competing_interpretations: disagreement may represent nesting, retracement or transition.
- evidence_refs: MTF_REASONING.md, K029-K032, FEATURE_DEFINITIONS_V1.
- claim_status: CORROBORATED conceptually; implementation pending.
- evaluation_tests: MTF conflict and no-future-leakage cases.
- decision_safety: contextual only.

## K010 — Invalidation
- type: reasoning_concept
- title: Invalidation
- definition: A predeclared observable condition that materially contradicts a hypothesis.
- operational_definition: Define the hypothesis, invalidation observation and action before outcome visibility.
- observable_inputs: hypothesis-specific measurements.
- data_requirements: causal measurements.
- applicable_conditions: any nontrivial hypothesis.
- weak_conditions: unmeasurable hypotheses.
- failure_modes: post-hoc invalidation.
- competing_interpretations: absence of evidence may be UNKNOWN rather than contradiction.
- evidence_refs: REASONING_CONSTITUTION.md, EVIDENCE_MODEL.md.
- claim_status: CORROBORATED as a reasoning principle.
- evaluation_tests: disconfirmation and outcome-blind tests.
- decision_safety: does not imply a trade.

## K011 — Stop Efficiency
- type: concept
- title: Stop Efficiency
- definition: Relationship between stop distance, thesis invalidation, volatility/noise and execution conditions.
- operational_definition: Evaluate only after the thesis invalidation reference and execution assumptions are explicit; numerical thresholds are versioned parameters, not universal rules.
- observable_inputs: invalidation level, price, volatility/noise, spread/execution conditions.
- data_requirements: causal price plus applicable execution data.
- applicable_conditions: trade construction/risk analysis.
- weak_conditions: unknown spread/depth, unclear thesis invalidation.
- failure_modes: optimizing stop distance without validating the thesis.
- competing_interpretations: wide stops may reduce noise sensitivity while increasing exposure; narrow stops may increase false invalidation.
- evidence_refs: TRADE_QUALITY_MODEL.md, RISK_EXECUTION_MODEL.md.
- claim_status: CORROBORATED conceptually; quantitative evaluation pending.
- evaluation_tests: stop-efficiency and execution-quality cases.
- decision_safety: never determines direction or size by itself.

## K012 — Evidence Conflict
- type: evidence_state
- title: Evidence Conflict
- definition: Material disagreement between observations, methods, sources or timeframes relevant to the same hypothesis.
- operational_definition: Preserve source identity, timestamps and conflicting observations; classify conflict using a versioned materiality criterion and return UNKNOWN when materiality cannot be established.
- observable_inputs: evidence provenance, observations, hypotheses.
- data_requirements: provenance metadata.
- applicable_conditions: competing-hypothesis evaluation.
- weak_conditions: missing provenance.
- failure_modes: averaging away disagreement or treating correlation as independence.
- competing_interpretations: apparent conflict may reflect different scales, venues or measurement semantics.
- evidence_refs: EVIDENCE_MODEL.md, DATA_QUALITY_CONTRACT.md.
- claim_status: CORROBORATED as evidence-discipline principle.
- evaluation_tests: cross-source disagreement and correlated-evidence cases.
- decision_safety: conflict constrains reasoning; it is not a signal.
