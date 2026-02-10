from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from journey2rich.config import get_settings


DEFAULT_NAMES: Dict[str, str] = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "GOOGL": "Alphabet",
    "META": "Meta",
    "NVDA": "Nvidia",
    "TSLA": "Tesla",
    "3067.HK": "iShares Hang Seng TECH ETF",
    "3690.HK": "Meituan",
}


@dataclass(frozen=True)
class Watchlist:
    tickers: List[str]
    names: Dict[str, str]


def load_watchlist() -> Watchlist:
    settings = get_settings()
    raw = settings.watchlist
    tickers = [t.strip() for t in raw.split(",") if t.strip()]
    names = {t: DEFAULT_NAMES.get(t, t) for t in tickers}
    return Watchlist(tickers=tickers, names=names)
