# Stage 2 Validation Report V2

Date: 2026-09-20
Scope: Data + Deterministic Observation

## Executive result

**STAGE 2 GATE: PASSED.**

The repository now contains an executable deterministic observation slice implementing the canonical F001-F018 contracts, deterministic tests, causal/no-future-leakage coverage, quality-state tests, timestamp/event tests, version recording, and a reproducible GitHub Actions test workflow.

## Implemented artifacts

- `src/xauusd_intelligence/features.py`
  - deterministic data/result models;
  - versioned feature results;
  - F001-F018 implementations;
  - timezone-aware timestamp enforcement;
  - causal cutoff enforcement;
  - confirmation-delay handling for structural swings;
  - explicit data-quality states;
  - broker activity explicitly labeled as a proxy;
  - volume provenance and proxy capability checks.
- `src/xauusd_intelligence/__init__.py`
- `tests/test_features.py`
- `pytest.ini`
- `.github/workflows/stage2-validation.yml`
- `src/xauusd_intelligence/README.md`

## Validation evidence

The implementation/test snapshot was executed locally with pytest:

**8 passed, 0 failed.**

Covered executable checks include:
1. all F001-F018 contracts are callable and return the correct feature identifiers;
2. future observations do not change an earlier causal result;
3. confirmed swings are unavailable before their confirmation timestamp;
4. invalid input propagates UNKNOWN/INVALID rather than being silently repaired;
5. stale, missing and insufficient-provenance inputs are explicitly classified;
6. event distance/window calculations use timestamp metadata only;
7. naive timestamps are rejected;
8. feature version is recorded in results.

A GitHub Actions workflow was added to run the same `pytest -q` suite on pushes to `main` and via manual dispatch. No Actions run was observable yet at validation time, so CI execution itself is not being represented as additional evidence.

## Contract coverage

### Data quality
PASS:
- VALID / STALE / MISSING / CONFLICTING / INVALID / UNKNOWN states are represented;
- stale and missing quote handling is executable;
- invalid spread handling is executable;
- missing provenance remains UNKNOWN;
- timestamps must be timezone-aware.

### Feature layer
PASS at implementation/test level:
- F001 OHLC Geometry
- F002 Returns
- F003 True Range
- F004 Realized Volatility
- F005 Volatility Baseline
- F006 Range Position
- F007 Confirmed Swing
- F008 Structural Reference
- F009 Structural Break
- F010 Structural Distance
- F011 Spread
- F012 Activity/Tick Proxy
- F013 Volume Provenance
- F014 Event Distance
- F015 Session State
- F016 MTF Synchronization
- F017 Event Window
- F018 Proxy Capability

### Causality
PASS for the implemented causal slice:
- every calculation receives an explicit cutoff;
- observations after the cutoff are excluded;
- a future mutation test leaves the earlier volatility result unchanged;
- structural swings are not exposed until their confirmation timestamp.

### Versioning
PASS:
- feature results carry the deterministic feature-layer version;
- configuration is represented by a versioned Config contract.

## Remaining limitations

Stage 2 is now a validated deterministic observation foundation, not a claim that all future production data adapters are complete.

Still required before live/forward use:
- real broker/feed adapter conformance tests;
- venue-specific timestamp/calendar adapters;
- production data freshness monitoring;
- broader property-based/adversarial test expansion;
- forward shadow validation of data behavior.

These are Stage 2 hardening/productionization work and do not authorize the reasoning engine or live execution.

## Gate decision

**Stage 2: PASSED.**

**Stage 4 remains blocked until the Stage 3 gate is explicitly verified against the current repository state.**

No reasoning engine, LLM trading logic, live execution integration, or performance claim was added.

## Commits

- `f89c595fd8df0ac94c72b73b5b1f17cbe8ff64bf` — deterministic F001-F018 implementation
- `049d9da13b8f9290b5c46926e3a9358917f4d53a` — package entrypoint
- `9d5a91f3023485b48433b80388e076f19d8a0a6b` — deterministic test suite
- `a4a4672ee57a5857e495955f833c590265223244` — pytest configuration
- `ec9a582d0d9f99b6e43553e9d2cd67c760e3ef12` — implementation documentation
- `eac934718d54e30d44a3c03a89898d04da1ae1a0` — expanded quality/timestamp/provenance tests
- `feb94358c73c27d1a8dfffed8911108017697117` — GitHub Actions validation workflow
