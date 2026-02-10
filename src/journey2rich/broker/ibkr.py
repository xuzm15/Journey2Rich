from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ib_insync import IB, Stock, MarketOrder


@dataclass
class IBKRPaperBroker:
    host: str
    port: int
    client_id: int

    def __post_init__(self) -> None:
        self.ib = IB()

    def connect(self) -> None:
        if not self.ib.isConnected():
            self.ib.connect(self.host, self.port, clientId=self.client_id)

    def disconnect(self) -> None:
        if self.ib.isConnected():
            self.ib.disconnect()

    def place_market_order(self, ticker: str, quantity: int, action: str = "BUY") -> Optional[int]:
        contract = Stock(ticker, "SMART", "USD")
        order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(contract, order)
        self.ib.sleep(1)
        return trade.order.orderId
