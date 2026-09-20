from datetime import datetime, timedelta, timezone
from xauusd_intelligence.features import *

def bars(n=35):
    t=datetime(2026,1,1,tzinfo=timezone.utc)
    return [Bar(t+timedelta(minutes=i),100+i,101+i,99+i,100.5+i,source="test",timeframe="1m") for i in range(n)]

def test_all_features_have_executable_contracts():
    bs=bars(); c=bs[-1].ts; q=[Quote(c,100,100.2,"test")]; e=Event(c+timedelta(minutes=10),"CPI")
    results=[
      f001_ohlc_geometry(bs[-1],c), f002_returns(bs,c), f003_true_range(bs,c),
      f004_realized_volatility(bs,c,5), f005_volatility_baseline(bs,c,3,3),
      f006_range_position(bs,c,10), f007_confirmed_swing(bs,c,2,2),
      f008_structural_reference(bs,c,2,2), f009_structural_break(bs,c,2,2),
      f010_structural_distance(bs,c,2,2), f011_spread(q,c,5),
      f012_activity_proxy(10,"broker",c),
      f013_volume_provenance(venue="broker",instrument="XAUUSD",source="feed",measurement="ticks",interval="1m",cutoff=c),
      f014_event_distance(c,e), f015_session_state(c,"london","cal-v1"),
      f016_mtf_synchronization({"1m":bs,"5m":bs[::5]},c),
      f017_event_window(c,e,900,900), f018_proxy_capability("order flow",{"trades"},{"ticks"},c)]
    assert [r.feature for r in results] == [f"F{i:03d}" for i in range(1,19)]

def test_no_future_leakage():
    bs=bars(20); cutoff=bs[10].ts
    before=f004_realized_volatility(bs,cutoff,5).value
    changed=bs[:]
    changed[15]=Bar(changed[15].ts,9999,10000,9998,9999.5,source="test")
    assert before == f004_realized_volatility(changed,cutoff,5).value

def test_confirmation_delay():
    bs=bars(10)
    bs[5]=Bar(bs[5].ts,100,110,99,100,source="test")
    bs[4]=Bar(bs[4].ts,100,105,99,100,source="test")
    bs[6]=Bar(bs[6].ts,100,104,99,100,source="test")
    assert f007_confirmed_swing(bs,bs[5].ts,2,2).quality == Quality.UNKNOWN
    assert f007_confirmed_swing(bs,bs[7].ts,2,2).quality == Quality.VALID

def test_quality_states_are_preserved():
    bs=bars(2)
    bs[1]=Bar(bs[1].ts,100,101,99,100.5,quality=Quality.INVALID)
    assert f002_returns(bs,bs[-1].ts).quality == Quality.UNKNOWN
    q=[Quote(bs[-1].ts,101,100,"x")]
    assert f011_spread(q,bs[-1].ts,5).quality == Quality.INVALID

def test_stale_missing_and_unknown_inputs():
    c=bars(1)[0].ts
    assert f011_spread([Quote(c-timedelta(seconds=10),100,100.1,"x")],c,5).quality == Quality.STALE
    assert f011_spread([Quote(c,None,100.1,"x")],c,5).quality == Quality.MISSING
    assert f013_volume_provenance(venue=None,instrument="XAUUSD",source="feed",measurement="ticks",interval="1m",cutoff=c).quality == Quality.UNKNOWN
    assert f018_proxy_capability("centralized trades",{"venue_trades"},{"broker_ticks"},c).value["capability"] == "UNKNOWN"

def test_timestamp_and_event_boundaries():
    c=datetime(2026,3,29,1,30,tzinfo=timezone.utc)
    e=Event(c+timedelta(seconds=600),"EVENT")
    assert f014_event_distance(c,e).value == 600
    assert f017_event_window(c,e,900,900).value == "pre-event"

def test_naive_timestamps_are_rejected():
    try:
        f014_event_distance(datetime(2026,1,1),None)
    except ValueError:
        pass
    else:
        assert False, "naive timestamps must be rejected"

def test_version_is_recorded():
    r=f012_activity_proxy(1,"feed",datetime.now(timezone.utc))
    assert r.version == VERSION
