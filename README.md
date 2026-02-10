# Journey2Rich

Fundamental-driven trading agent for US equities and options using IBKR paper trading.

## What this includes (v0.1)
- Pluggable data providers (initially `yfinance` for fundamentals, prices, options chains).
- IBKR paper trading connector via `ib_insync`.
- Simple fundamental quality screen + price filter to generate a watchlist.
- Minimal backtest scaffold (daily bar, long-only).
- CLI to run a backtest or paper-trading loop.

## Quick start
1. Install dependencies
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. Configure environment
   ```bash
   cp .env.example .env
   ```
   Edit `.env` for IBKR connection params if needed.

3. Backtest (toy example)
   ```bash
   journey2rich backtest --tickers AAPL,MSFT,GOOGL --start 2019-01-01 --end 2024-01-01
   ```

4. Push a daily brief to Discord (one-off)
   ```bash
   journey2rich push
   ```

5. Run daily scheduler (08:00 in TIMEZONE)
   ```bash
   journey2rich schedule
   ```

6. Paper trading (requires TWS/IB Gateway running)
   ```bash
   journey2rich paper --tickers AAPL,MSFT
   ```

## Notes on data
- `yfinance` is convenient for prototyping; for production-quality fundamentals and options you should swap to a paid provider.
- The data layer is intentionally abstracted for easy replacement.

## IBKR setup (paper)
- Install TWS or IB Gateway.
- Enable API access and set a trusted IP.
- Default paper port is usually `7497`.

## Next steps
- Add a more robust fundamental model (valuation + quality + momentum).
- Introduce risk limits, portfolio sizing, and options selection logic.
- Add scheduling and execution guardrails.
