# Case G — WAIT Opportunity Cost

## Purpose
Prevent learning systems from concluding that WAIT is always optimal.

## Setup
Two opportunities occur in a sequence: the first is incomplete and should be rejected; the second later satisfies the declared evidence and risk requirements.

## Expected invariants
- Reject the first for explicit reasons.
- Remain capable of recognizing the second.
- Log both decisions and their outcomes.
- Measure missed opportunity separately from avoided bad exposure.
