from __future__ import annotations

import pandas as pd

from .providers import DataProvider


def load_price_history(provider: DataProvider, ticker: str, start: str, end: str) -> pd.DataFrame:
    return provider.get_price_history(ticker, start, end)
