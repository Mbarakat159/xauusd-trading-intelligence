# Evidence and Uncertainty Model

The knowledge layer must distinguish evidence from interpretation.

## Evidence classes

E0 — raw observation: price crossed a prior high.

E1 — derived measurement: range expanded to 1.8x recent median range.

E2 — model interpretation: volatility appears to be transitioning from compression to expansion.

E3 — framework hypothesis: the move resembles a Wyckoff spring.

E4 — empirical research claim: a claim supported by a documented study, with population, sample and assumptions recorded.

E5 — practitioner or marketing claim: useful for hypothesis generation but weak until independently supported.

## Confidence is multidimensional

Do not store one generic confidence number.

Track at least:
- observation reliability;
- source quality;
- interpretation uncertainty;
- regime fit;
- conflicting evidence;
- data completeness;
- execution uncertainty.

An LLM subjective confidence is not a calibrated probability of profit and must never independently determine position size.

## Contradiction protocol

When evidence conflicts:
1. preserve both observations;
2. determine whether they refer to different horizons;
3. determine whether one is stale;
4. inspect data quality;
5. generate alternative hypotheses;
6. identify the observation that would discriminate between them;
7. keep the conflict visible if unresolved.

## Provenance requirements

Each knowledge claim should ideally carry:
- source;
- source class;
- market/instrument;
- timeframe;
- sample period;
- assumptions;
- evidence type;
- limitations;
- independent corroboration;
- last review date.

## Knowledge lifecycle

discovered -> extracted -> normalized -> challenged -> corroborated -> accepted/restricted -> monitored

Accepted means accepted into the knowledge base as a reusable concept, not accepted as a profitable trading rule.
