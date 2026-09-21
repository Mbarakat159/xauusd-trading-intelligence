# cTrader XAUUSD connectivity test

This is a one-shot integration probe. It is not part of the Stage 7 decision engine and does not place orders.

## What it proves

The probe verifies, in order:

1. cTrader Open API application authentication.
2. Pepperstone Demo account authentication.
3. Symbol discovery for the authenticated account.
4. XAUUSD symbol resolution.
5. Spot subscription.
6. Receipt of a current XAUUSD bid/ask event.

cTrader documents `ProtoOASymbolsListReq` for account symbol discovery and `ProtoOASubscribeSpotsReq` for live bid/ask events. The first spot event after subscription contains the latest spot price even when the market is closed.

## Required local secrets

Do NOT put these in GitHub, commit them, or send them in chat.

Set locally:

- `CTRADER_CLIENT_ID`
- `CTRADER_CLIENT_SECRET`
- `CTRADER_ACCESS_TOKEN`
- `CTRADER_ACCOUNT_ID=48758507`

The current token must have **Account info** scope.

## Run

Install the official Spotware Python SDK:

```bash
python -m pip install ctrader-open-api
```

From the repository root:

### PowerShell

```powershell
$env:CTRADER_CLIENT_ID="YOUR_CLIENT_ID"
$env:CTRADER_CLIENT_SECRET="YOUR_CLIENT_SECRET"
$env:CTRADER_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
$env:CTRADER_ACCOUNT_ID="48758507"

python tools/ctrader_connectivity_test.py
```

### Windows CMD

```cmd
set CTRADER_CLIENT_ID=YOUR_CLIENT_ID
set CTRADER_CLIENT_SECRET=YOUR_CLIENT_SECRET
set CTRADER_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
set CTRADER_ACCOUNT_ID=48758507

python tools/ctrader_connectivity_test.py
```

The script connects to the cTrader **Demo** Protobuf endpoint `demo.ctraderapi.com:5035`. Demo and live endpoints are separate.

## Expected successful output

```text
Connecting to cTrader Open API...
1/5 application authentication: OK
2/5 account authentication: OK
3/5 symbol discovery: OK — XAUUSD ... (symbolId=...)
4/5 spot subscription: OK — waiting for first spot event
5/5 XAUUSD spot: OK — bid=... ask=...
RESULT: cTrader Open API can deliver XAUUSD market data to the client.
```

Do not paste any credential values into the repository.

## Interpretation

A successful run proves the connectivity path:

`cTrader Open API → authenticated demo account → XAUUSD → live quote`

It does **not** yet prove Stage 7, the Causal Market Replay Lab, or trading profitability.
