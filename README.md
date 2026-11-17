# SENTINEL V10 — Settlement Edition (PAPER ONLY)

## What's changed
- **Balanced** entry scoring: BTC 1m candles (Coinbase > Kraken > Bitstamp > recent-trades recovery), moving averages, RSI, VWAP, volatility, strike distance, momentum, Kalshi book. Scores are heuristic strength, **not actual 75% probabilities**.
- **Settlement exits only**: once simulated paper buy is recorded, the trade stays OPEN until Kalshi market API reports official `result=yes` or `result=no`. It closes at 100¢ or 0¢. No TP, SL, or early sale. Closed/unresolved markets remain OPEN (pending).
- **Max one entry per ticker**: enforced by SQLite UNIQUE(ticker); only active nearest-expiring `KXBTC15M` ticker is considered. The bot aims to trade once in the minute-9-to-12 window, but skips when market, freshness, liquidity, or safety checks fail; **cannot guarantee one trade each interval**.
- Simulates immediate buy at best executable Kalshi ask plus 0.5¢ adverse slippage, checks best ask depth, spread, and cash. Estimates general taker fee per order `ceil(0.07 * contracts * price*(1-price) * 100)/100`. Actual Kalshi fees can vary by market or fee schedule; verify. Settlement has no sell order/exit fee. P&L is not a verified historical fill or a real trade.
- Tracks entry/official exit prices, signals/evidence, net P&L, 95% Wilson win-rate interval, 75% target comparison, trade CSV, current interval WAIT/SKIP reasons. All simulated, no API credentials, no order placement.

## iPhone + GitHub + Streamlit Cloud
1. Unzip this package in iPhone Files.
2. For a **new repo**, upload `app.py`, `engine.py`, `requirements.txt`, `report.py`, `worker.py`, and the `.streamlit/config.toml` if possible. For an existing repo, replace **app.py and engine.py together**, and ensure `requirements.txt` includes `streamlit`, `streamlit-autorefresh`, `pandas`, `requests`.
3. In Streamlit Community Cloud, select GitHub repository, branch, and `app.py`. Open the URL on iPhone, optionally Add to Home Screen.
4. This is phone-accessible, NOT reliable 24/7 hosting. Streamlit Cloud may sleep/redeploy; its **local SQLite is ephemeral**. Your trades can vanish after app recreation. Never count retained trades as a complete sample without durable storage.
5. This edition uses a DIFFERENT default SQLite file (`sentinel_v10_settlement.sqlite3`) to avoid mixing hybrid and settlement performance. Do not overwrite your original DB; if upgrading on the same existing Cloud repo, the new DB starts empty.

## Windows + durable local history
Extract folder on Windows. Double-click `START_WORKER_WINDOWS.bat` then `START_DASHBOARD_WINDOWS.bat` (requires installed Python and `py` launcher). Both share local SQLite in this folder, surviving ordinary restarts while the files remain. Keep worker running and PC awake for ongoing scans; app does not run while shut down.

## Testing the goal
`python -m unittest discover -s tests -v` for offline tests, and `python report.py` for recorded paper results. The reported 95% Wilson interval cannot establish a stable strategy from a few trades. At least ~500 forward observations is a useful initial evaluation, not proof. Analyze skipped intervals and actual realized NET P&L after entry friction and fees. **75% is a target, never a promise.**

## Safety / data caveats
Exchange BTC/USD is a *proxy*, not Kalshi's CF Benchmarks official settlement price. Market `result` is authoritative. The feed guard rejects stale OHLC; stale feeds block NEW entries, but do not prevent the official settlement check. The built-in phone-hosted worker is a best-effort in-process thread only. For independent, truly persistent all-day scans and history, use an always-on remote worker with durable database, which this ZIP does not deploy.
