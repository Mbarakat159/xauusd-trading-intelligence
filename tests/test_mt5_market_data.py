from datetime import datetime, timezone

import pytest

from xauusd_intelligence.mt5_market_data import MT5MarketDataAdapter


class FakeMT5:
    def __init__(self, visible=True):
        self.initialized = False
        self.shutdown_called = False
        self.selected = False
        self.info = type("Info", (), {"visible": visible})()
        self.tick = type(
            "Tick",
            (),
            {"bid": 4347.39, "ask": 4347.66, "time": 1789993366},
        )()
        self.rates = [
            {
                "time": 1789993320,
                "open": 4346.37,
                "high": 4347.45,
                "low": 4346.34,
                "close": 4347.39,
                "tick_volume": 319,
            }
        ]

    def initialize(self):
        self.initialized = True
        return True

    def shutdown(self):
        self.shutdown_called = True

    def symbol_info(self, symbol):
        return self.info

    def symbol_select(self, symbol, enable):
        self.selected = enable
        return True

    def symbol_info_tick(self, symbol):
        return self.tick

    def copy_rates_from_pos(self, symbol, timeframe, start_pos, count):
        return self.rates


def adapter(fake):
    return MT5MarketDataAdapter(fake, timeframes={"M1": 1, "H1": 16385})


def test_connect_and_close_are_forwarded():
    fake = FakeMT5()
    a = adapter(fake)
    a.connect()
    a.close()
    assert fake.initialized is True
    assert fake.shutdown_called is True


def test_invisible_symbol_is_selected():
    fake = FakeMT5(visible=False)
    adapter(fake).ensure_symbol()
    assert fake.selected is True


def test_snapshot_normalizes_tick_and_bars():
    snapshot = adapter(FakeMT5()).snapshot(count=1)
    assert snapshot.symbol == "XAUUSD.sd"
    assert snapshot.tick.bid == pytest.approx(4347.39)
    assert snapshot.tick.ask == pytest.approx(4347.66)
    assert snapshot.tick.time.tzinfo == timezone.utc
    assert snapshot.bars["M1"][0].close == pytest.approx(4347.39)
    assert snapshot.bars["M1"][0].tick_volume == 319
    assert snapshot.bars["H1"][0].time.tzinfo == timezone.utc


def test_missing_symbol_is_rejected():
    fake = FakeMT5()
    fake.info = None
    with pytest.raises(LookupError, match="symbol not found"):
        adapter(fake).ensure_symbol()


def test_empty_bars_are_rejected():
    fake = FakeMT5()
    fake.rates = []
    with pytest.raises(LookupError, match="no bars returned"):
        adapter(fake).read_bars("M1", 1)


def test_non_positive_count_is_rejected():
    with pytest.raises(ValueError, match="count must be positive"):
        adapter(FakeMT5()).read_bars("M1", 1, 0)
