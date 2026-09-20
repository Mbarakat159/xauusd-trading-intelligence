# Stage 2 deterministic observation implementation

This package is the executable validation slice for the existing Stage 2 contracts.

Implemented canonical features: F001-F018.

Design constraints:
- every result is timestamped and versioned;
- timestamps must be timezone-aware;
- calculations use only observations at or before the declared cutoff;
- missing/invalid/stale/conflicting/unknown inputs are never silently fabricated;
- confirmed structures become available only at their declared confirmation timestamp;
- broker tick activity is explicitly labeled as a proxy;
- volume provenance is preserved;
- event features expose timing metadata, not event outcomes.

This is an observation layer only. It does not generate trades, sizing, entries, exits, or execution commands.
