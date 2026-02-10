from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

from journey2rich.broker.ibkr import IBKRPaperBroker
from journey2rich.config import get_settings
from journey2rich.data import YFinanceProvider
from journey2rich.strategies.fundamental_quality import generate_signal


def run_paper(tickers: List[str], quantity: int = 1) -> List[Dict]:
    settings = get_settings()
    provider = YFinanceProvider()
    broker = IBKRPaperBroker(settings.ibkr_host, settings.ibkr_port, settings.ibkr_client_id)

    end = datetime.utcnow().date()
    start = end - timedelta(days=365 * 3)

    results: List[Dict] = []
    broker.connect()
    try:
        for ticker in tickers:
            signal = generate_signal(provider, ticker, start.isoformat(), end.isoformat())
            if signal.get("signal") == "BUY":
                order_id = broker.place_market_order(ticker, quantity, action="BUY")
                results.append({"ticker": ticker, "action": "BUY", "order_id": order_id})
            elif signal.get("signal") == "SELL":
                order_id = broker.place_market_order(ticker, quantity, action="SELL")
                results.append({"ticker": ticker, "action": "SELL", "order_id": order_id})
            else:
                results.append({"ticker": ticker, "action": "HOLD"})
    finally:
        broker.disconnect()

    return results
