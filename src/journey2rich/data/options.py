from __future__ import annotations

from typing import Dict, Optional

from .providers import DataProvider


def load_options_chain(provider: DataProvider, ticker: str, expiry: Optional[str] = None) -> Dict:
    return provider.get_options_chain(ticker, expiry)
