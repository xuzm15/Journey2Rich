from __future__ import annotations

from typing import Dict, Optional

import pandas as pd


def _pick_otm_call(chain: pd.DataFrame, spot: float) -> Optional[Dict]:
    if chain.empty or "strike" not in chain.columns:
        return None
    calls = chain[chain["strike"] > spot * 1.05].sort_values("strike")
    if calls.empty:
        return None
    row = calls.iloc[0]
    return {
        "strike": float(row["strike"]),
        "lastPrice": float(row.get("lastPrice") or 0.0),
        "impliedVolatility": float(row.get("impliedVolatility") or 0.0),
    }


def _pick_otm_put(chain: pd.DataFrame, spot: float) -> Optional[Dict]:
    if chain.empty or "strike" not in chain.columns:
        return None
    puts = chain[chain["strike"] < spot * 0.95].sort_values("strike", ascending=False)
    if puts.empty:
        return None
    row = puts.iloc[0]
    return {
        "strike": float(row["strike"]),
        "lastPrice": float(row.get("lastPrice") or 0.0),
        "impliedVolatility": float(row.get("impliedVolatility") or 0.0),
    }


def build_option_suggestions(spot: Optional[float], options: Dict, signal: str) -> Dict[str, str]:
    if spot is None:
        return {"directional": "", "income": ""}
    calls = options.get("calls") if options else None
    puts = options.get("puts") if options else None
    expiry = options.get("expiry") if options else None
    directional = ""
    income = ""

    if isinstance(calls, pd.DataFrame) and isinstance(puts, pd.DataFrame):
        if signal == "BUY":
            call = _pick_otm_call(calls, spot)
            if call:
                directional = f"Buy call ~{call['strike']:.2f} exp {expiry}"
        elif signal == "SELL":
            put = _pick_otm_put(puts, spot)
            if put:
                directional = f"Buy put ~{put['strike']:.2f} exp {expiry}"

        # Income idea (covered call) for BUY/HOLD
        if signal in {"BUY", "HOLD"}:
            call = _pick_otm_call(calls, spot)
            if call:
                income = f"Sell covered call ~{call['strike']:.2f} exp {expiry}"

    return {"directional": directional, "income": income}
