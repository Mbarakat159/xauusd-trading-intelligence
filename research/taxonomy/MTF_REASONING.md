# Multi-Timeframe Reasoning Model

MTF analysis is a relationship model, not a stack of independent signals.

## Roles are dynamic

A timeframe may contribute:
- broad context;
- structural map;
- setup location;
- trigger;
- execution detail;
- invalidation refinement;
- volatility/execution information.

These roles should be learned or selected from market state rather than permanently assigned as 4H equals trend and 5M equals entry.

## Relationship graph

For each observation, preserve:

timeframe -> structure -> location -> hypothesis -> trigger -> invalidation -> expected path

The system must know which lower-timeframe event is relevant to which higher-timeframe hypothesis.

## Conflict handling

Example:
- higher timeframe: directional continuation;
- intermediate timeframe: range;
- lower timeframe: bearish break.

The engine should not count these as votes. It should ask:
- Is the lower-timeframe move a pullback, genuine structural failure, or noise?
- Where is the higher-timeframe invalidation?
- Did price accept or reject the new area?
- Does volatility/event context support continuation or transition?

## Information roles

Higher timeframes can provide structural context, major reference zones, and broader volatility/regime information.

Lower timeframes can provide execution timing, local rejection/displacement, microstructure proxies, and tighter invalidation when justified.

This does not imply higher timeframe always dominates. The relevant relationship depends on the holding horizon and hypothesis.

## MTF failure modes

Avoid:
- majority-vote timeframe systems;
- fixed all-timeframes-must-agree rules;
- lower-timeframe triggers without a defined higher-timeframe thesis;
- treating every timeframe as independent evidence;
- changing timeframe until a desired narrative appears.

## Required audit trail

Every MTF conclusion should record:
- timeframes inspected;
- role assigned to each;
- observations;
- conflicts;
- final hypothesis;
- invalidation;
- reason additional timeframes were or were not inspected.
