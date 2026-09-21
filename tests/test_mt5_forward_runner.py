from datetime import datetime, timezone
import json

from xauusd_intelligence.mt5_forward_runner import ForwardRunner
from xauusd_intelligence.mt5_market_data import MarketBar, MarketSnapshot, MarketTick


class FakeAdapter:
    def __init__(self, snapshots, failures=()):
        self.snapshots = list(snapshots)
        self.failures = list(failures)
        self.connected = 0
        self.closed = 0

    def connect(self):
        self.connected += 1

    def close(self):
        self.closed += 1

    def snapshot(self, count=100):
        if self.failures:
            raise self.failures.pop(0)
        return self.snapshots.pop(0)


def snapshot(ts):
    tick = MarketTick("XAUUSD.sd", 4350.0, 4350.3, ts)
    bars = (
        MarketBar(
            "XAUUSD.sd", "M1", ts, 4349.0, 4351.0, 4348.5, 4350.0, 120
        ),
    )
    return MarketSnapshot("XAUUSD.sd", tick, {"M1": bars})


def test_runner_persists_causal_observations(tmp_path):
    times = [
        datetime(2026, 9, 21, 19, 30, tzinfo=timezone.utc),
        datetime(2026, 9, 21, 19, 31, tzinfo=timezone.utc),
    ]
    adapter = FakeAdapter([snapshot(times[0]), snapshot(times[1])])
    now_values = iter(times + times)
    runner = ForwardRunner(
        adapter,
        output_path=tmp_path / "observations.jsonl",
        symbol="XAUUSD.sd",
        source="MetaTrader5",
        venue="EquitiBrokerageSC-Demo",
        interval_seconds=1,
        bar_count=20,
        now=lambda: next(now_values),
        sleep=lambda _: None,
    )

    assert runner.run(max_observations=2) == 2
    assert adapter.connected == 1
    assert adapter.closed == 1

    records = [
        json.loads(line)
        for line in (tmp_path / "observations.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(records) == 2
    assert all(r["record_type"] == "shadow_observation" for r in records)
    assert records[0]["observation"]["as_of"].startswith("2026-09-21T19:30:00")
    assert records[1]["observation"]["as_of"].startswith("2026-09-21T19:31:00")
    assert records[0]["observation"]["feature_version"] == "deterministic-features-v1.0.0"
    assert records[0]["observation"]["reasoning_version"] == "reasoning-engine-v1.0.0"
    assert records[0]["observation"]["safety_version"] == "decision-risk-execution-safety-v1.0.0"


def test_runner_reconnects_after_source_failure_without_synthetic_observation(tmp_path):
    ts = datetime(2026, 9, 21, 19, 40, tzinfo=timezone.utc)
    adapter = FakeAdapter(
        [snapshot(ts)],
        failures=[ConnectionError("temporary MT5 disconnect")],
    )
    runner = ForwardRunner(
        adapter,
        output_path=tmp_path / "observations.jsonl",
        symbol="XAUUSD.sd",
        source="MetaTrader5",
        venue="EquitiBrokerageSC-Demo",
        interval_seconds=1,
        bar_count=20,
        now=lambda: ts,
        sleep=lambda _: None,
    )

    assert runner.run(max_observations=1) == 1
    assert adapter.connected == 2
    assert adapter.closed == 2

    records = [
        json.loads(line)
        for line in (tmp_path / "observations.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert [r["record_type"] for r in records] == ["source_error", "shadow_observation"]
    assert "temporary MT5 disconnect" in records[0]["error"]
