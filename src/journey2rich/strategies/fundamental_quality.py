from __future__ import annotations

from typing import Dict

import pandas as pd

from journey2rich.data.fundamentals import score_fundamentals
from journey2rich.data.providers import DataProvider


def generate_signal(
    provider: DataProvider,
    ticker: str,
    start: str,
    end: str,
    score_threshold: float = 3.0,
    sell_threshold: float = 1.0,
) -> Dict:
    info = provider.get_fundamentals(ticker)
    score = score_fundamentals(info)

    prices = provider.get_price_history(ticker, start, end)
    if prices.empty or "Close" not in prices.columns:
        return {"ticker": ticker, "signal": "HOLD", "reason": "no_price_data", "score": score, "price": None}

    closes = prices["Close"].astype(float)
    if len(closes) < 210:
        return {
            "ticker": ticker,
            "signal": "HOLD",
            "reason": "insufficient_history",
            "score": score,
            "price": float(closes.iloc[-1]),
        }

    sma_50 = closes.rolling(50).mean().iloc[-1]
    sma_200 = closes.rolling(200).mean().iloc[-1]
    last_close = closes.iloc[-1]

    if score["score"] >= score_threshold and sma_50 > sma_200 and last_close > sma_50:
        return {
            "ticker": ticker,
            "signal": "BUY",
            "reason": "score_and_trend",
            "score": score,
            "price": float(last_close),
        }

    if score["score"] <= sell_threshold and sma_50 < sma_200 and last_close < sma_50:
        return {
            "ticker": ticker,
            "signal": "SELL",
            "reason": "weak_score_and_trend_down",
            "score": score,
            "price": float(last_close),
        }

    return {
        "ticker": ticker,
        "signal": "HOLD",
        "reason": "filters_not_met",
        "score": score,
        "price": float(last_close),
    }
