from __future__ import annotations

from typing import Dict


def score_fundamentals(info: Dict) -> Dict:
    """
    Return a simple fundamental score from yfinance 'info'.
    This is a heuristic model using quality, value, growth, and leverage signals.
    """
    # Defensive defaults
    market_cap = float(info.get("marketCap") or 0)
    pe = float(info.get("trailingPE") or 0)
    fwd_pe = float(info.get("forwardPE") or 0)
    ev_to_ebitda = float(info.get("enterpriseToEbitda") or 0)
    roe = float(info.get("returnOnEquity") or 0)
    roic = float(info.get("returnOnAssets") or 0)
    margin = float(info.get("profitMargins") or 0)
    gross_margin = float(info.get("grossMargins") or 0)
    revenue_growth = float(info.get("revenueGrowth") or 0)
    earnings_growth = float(info.get("earningsQuarterlyGrowth") or 0)
    debt_to_equity = float(info.get("debtToEquity") or 0)
    current_ratio = float(info.get("currentRatio") or 0)

    # Quality: ROE/ROA, margins
    quality = 0.0
    if roe > 0.12:
        quality += 1.0
    if roic > 0.06:
        quality += 0.5
    if margin > 0.10:
        quality += 1.0
    if gross_margin > 0.35:
        quality += 0.5

    # Value: PE/EV-EBITDA
    value = 0.0
    if 0 < pe < 25:
        value += 1.0
    elif 0 < fwd_pe < 22:
        value += 1.0
    if 0 < ev_to_ebitda < 18:
        value += 1.0

    # Growth: revenue/earnings
    growth = 0.0
    if revenue_growth > 0.08:
        growth += 1.0
    if earnings_growth > 0.10:
        growth += 1.0

    # Leverage/Liquidity
    leverage = 0.0
    if 0 < debt_to_equity < 150:
        leverage += 1.0
    if current_ratio > 1.2:
        leverage += 0.5

    # Size bonus (liquidity proxy)
    size = 0.0
    if market_cap > 1e10:
        size += 0.5

    score = quality + value + growth + leverage + size

    return {
        "score": score,
        "marketCap": market_cap,
        "trailingPE": pe,
        "forwardPE": fwd_pe,
        "enterpriseToEbitda": ev_to_ebitda,
        "returnOnEquity": roe,
        "returnOnAssets": roic,
        "profitMargins": margin,
        "grossMargins": gross_margin,
        "revenueGrowth": revenue_growth,
        "earningsQuarterlyGrowth": earnings_growth,
        "debtToEquity": debt_to_equity,
        "currentRatio": current_ratio,
        "qualityScore": quality,
        "valueScore": value,
        "growthScore": growth,
        "leverageScore": leverage,
    }
