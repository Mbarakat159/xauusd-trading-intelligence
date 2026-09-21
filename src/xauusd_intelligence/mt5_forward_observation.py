"""Build causal forward-shadow observations from read-only MT5 snapshots.

This module only converts market data already observed at time T into the
frozen observation contract. It does not calculate outcomes, submit orders,
or expose future market information.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone

from .mt5_market_data import MarketSnapshot
from .shadow import ShadowObservation, digest_payload

VERSION = "mt5-forward-observation-v1.0.0"


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("naive timestamp is not allowed")
    return dt.astimezone(timezone.utc)


def _snapshot_payload(snapshot: MarketSnapshot) -> dict:
    return {
        "symbol": snapshot.symbol,
        "tick": asdict(snapshot.tick),
        "bars": {
            timeframe: [asdict(bar) for bar in bars]
            for timeframe, bars in sorted(snapshot.bars.items())
        },
    }


def build_shadow_observation(
    snapshot: MarketSnapshot,
    *,
    source: str,
    venue: str | None,
    feature_version: str,
    reasoning_version: str,
    safety_version: str,
) -> ShadowObservation:
    """Convert one MT5 snapshot into one immutable forward observation.

    The observation timestamp is the snapshot tick time. The payload digest and
    observation ID are derived only from data available in that snapshot.
    """
    if not source:
        raise ValueError("source is required")
    if not feature_version:
        raise ValueError("feature_version is required")
    if not reasoning_version:
        raise ValueError("reasoning_version is required")
    if not safety_version:
        raise ValueError("safety_version is required")
    if snapshot.tick.symbol != snapshot.symbol:
        raise ValueError("snapshot tick symbol does not match snapshot symbol")

    payload = _snapshot_payload(snapshot)
    payload_digest = digest_payload(payload)
    timestamp = _utc(snapshot.tick.time)
    observation_id = f"mt5:{snapshot.symbol}:{timestamp.isoformat()}:{payload_digest[:16]}"

    return ShadowObservation(
        observation_id=observation_id,
        as_of=timestamp,
        symbol=snapshot.symbol,
        source=source,
        venue=venue,
        payload_digest=payload_digest,
        feature_version=feature_version,
        reasoning_version=reasoning_version,
        safety_version=safety_version,
    )
