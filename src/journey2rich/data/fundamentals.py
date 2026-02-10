from __future__ import annotations

from typing import Dict


def score_fundamentals(info: Dict) -> Dict:
    """
    Return a simple fundamental score from yfinance 'info'.
    This is a placeholder and should be replaced with a robust model.
    """
    # Defensive defaults
    market_cap = float(info.get("marketCap") or 0)
    pe = float(info.get("trailingPE") or 0)
    roe = float(info.get("returnOnEquity") or 0)
    margin = float(info.get("profitMargins") or 0)
    debt_to_equity = float(info.get("debtToEquity") or 0)

    # Simple heuristic scoring
    score = 0.0
    if market_cap > 1e10:
        score += 1.0
    if 0 < pe < 30:
        score += 1.0
    if roe > 0.12:
        score += 1.0
    if margin > 0.10:
        score += 1.0
    if debt_to_equity and debt_to_equity < 150:
        score += 1.0

    return {
        "score": score,
        "marketCap": market_cap,
        "trailingPE": pe,
        "returnOnEquity": roe,
        "profitMargins": margin,
        "debtToEquity": debt_to_equity,
    }
