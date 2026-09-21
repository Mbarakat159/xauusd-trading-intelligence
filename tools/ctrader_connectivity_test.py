"""One-shot cTrader Open API connectivity probe.

This script is intentionally outside the intelligence pipeline. It verifies:
1) application authentication,
2) account authentication,
3) account symbol discovery,
4) XAUUSD symbol resolution,
5) current spot subscription,
6) one live bid/ask event.

Credentials are read ONLY from environment variables and are never printed.

Required environment variables:
  CTRADER_CLIENT_ID
  CTRADER_CLIENT_SECRET
  CTRADER_ACCESS_TOKEN
  CTRADER_ACCOUNT_ID

The access token should have Account info scope for this read-only test.
"""

from __future__ import annotations

import os
import sys
import time

from ctrader_open_api import Client, EndPoints, Protobuf, TcpProtocol
from ctrader_open_api.messages.OpenApiMessages_pb2 import (
    ProtoOAAccountAuthReq,
    ProtoOAAccountAuthRes,
    ProtoOAApplicationAuthReq,
    ProtoOAApplicationAuthRes,
    ProtoOASpotEvent,
    ProtoOASubscribeSpotsReq,
    ProtoOASubscribeSpotsRes,
    ProtoOASymbolsListReq,
    ProtoOASymbolsListRes,
)
from ctrader_open_api.messages.OpenApiModelMessages_pb2 import ProtoOASymbol


def required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing environment variable: {name}")
    return value


CLIENT_ID = required("CTRADER_CLIENT_ID")
CLIENT_SECRET = required("CTRADER_CLIENT_SECRET")
ACCESS_TOKEN = required("CTRADER_ACCESS_TOKEN")
ACCOUNT_ID = int(required("CTRADER_ACCOUNT_ID"))

client = Client(EndPoints.PROTOBUF_LIVE_HOST, EndPoints.PROTOBUF_PORT, TcpProtocol)
state = {"symbol_id": None, "symbol_name": None, "spot": None}


def on_error(failure):
    print("ERROR:", failure)
    client.stopService()


def on_message(message):
    payload = message.payloadType

    if payload == ProtoOAApplicationAuthRes().payloadType:
        print("1/5 application authentication: OK")
        req = ProtoOAAccountAuthReq()
        req.ctidTraderAccountId = ACCOUNT_ID
        req.accessToken = ACCESS_TOKEN
        client.send(req)

    elif payload == ProtoOAAccountAuthRes().payloadType:
        print("2/5 account authentication: OK")
        req = ProtoOASymbolsListReq()
        req.ctidTraderAccountId = ACCOUNT_ID
        client.send(req)

    elif payload == ProtoOASymbolsListRes().payloadType:
        res = Protobuf.extract(message)
        matches = []
        for symbol in res.symbol:
            name = getattr(symbol, "symbolName", "")
            if name.upper() == "XAUUSD" or "XAUUSD" in name.upper():
                matches.append(symbol)

        if not matches:
            print("3/5 symbol discovery: FAILED — no XAUUSD-like symbol returned")
            client.stopService()
            return

        symbol = matches[0]
        state["symbol_id"] = int(symbol.symbolId)
        state["symbol_name"] = symbol.symbolName
        print(f"3/5 symbol discovery: OK — {symbol.symbolName} (symbolId={symbol.symbolId})")

        req = ProtoOASubscribeSpotsReq()
        req.ctidTraderAccountId = ACCOUNT_ID
        req.symbolId.append(symbol.symbolId)
        client.send(req)

    elif payload == ProtoOASubscribeSpotsRes().payloadType:
        print("4/5 spot subscription: OK — waiting for first spot event")

    elif payload == ProtoOASpotEvent().payloadType:
        res = Protobuf.extract(message)
        bid = getattr(res, "bid", None)
        ask = getattr(res, "ask", None)
        state["spot"] = (bid, ask)
        digits = 5
        print(f"5/5 XAUUSD spot: OK — bid={bid} ask={ask} (raw API values)")
        print("RESULT: cTrader Open API can deliver XAUUSD market data to the client.")
        client.stopService()


client.setConnectedCallback(lambda _: authenticate())
client.setMessageReceivedCallback(on_message)
client.setDisconnectedCallback(lambda _: print("Disconnected."))
client.setErrorCallback(on_error)


def authenticate():
    req = ProtoOAApplicationAuthReq()
    req.clientId = CLIENT_ID
    req.clientSecret = CLIENT_SECRET
    client.send(req)


print("Connecting to cTrader Open API...")
client.startService()
time.sleep(15)

if state["spot"] is None:
    print("TIMEOUT: no XAUUSD spot event received within the test window.")
    sys.exit(2)
