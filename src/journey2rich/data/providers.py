from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import pandas as pd
import yfinance as yf


class DataProvider:
    def get_fundamentals(self, ticker: str) -> Dict:
        raise NotImplementedError

    def get_price_history(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        raise NotImplementedError

    def get_options_chain(self, ticker: str, expiry: Optional[str] = None) -> Dict:
        raise NotImplementedError


@dataclass
class YFinanceProvider(DataProvider):
    def get_fundamentals(self, ticker: str) -> Dict:
        t = yf.Ticker(ticker)
        info = t.get_info() or {}
        return info

    def get_price_history(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        t = yf.Ticker(ticker)
        df = t.history(start=start, end=end, auto_adjust=False)
        if df is None:
            return pd.DataFrame()
        df = df.reset_index()
        return df

    def get_options_chain(self, ticker: str, expiry: Optional[str] = None) -> Dict:
        t = yf.Ticker(ticker)
        if expiry is None:
            expiries = t.options
            if not expiries:
                return {"calls": pd.DataFrame(), "puts": pd.DataFrame(), "expiry": None}
            expiry = expiries[0]
        chain = t.option_chain(expiry)
        return {"calls": chain.calls, "puts": chain.puts, "expiry": expiry}
