from __future__ import annotations

from typing import Dict

import pandas as pd

from journey2rich.data.providers import DataProvider
from journey2rich.strategies.fundamental_quality import generate_signal


def run_backtest(provider: DataProvider, ticker: str, start: str, end: str) -> Dict:
    signal = generate_signal(provider, ticker, start, end)
    prices = provider.get_price_history(ticker, start, end)
    if prices.empty:
        return {"ticker": ticker, "status": "no_data"}

    prices = prices.sort_values("Date")
    prices["Return"] = prices["Close"].pct_change().fillna(0.0)
    total_return = (1.0 + prices["Return"]).prod() - 1.0

    return {
        "ticker": ticker,
        "signal": signal["signal"],
        "total_return": float(total_return),
        "bars": int(len(prices)),
        "score": signal["score"],
    }
