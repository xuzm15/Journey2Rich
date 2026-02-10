from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from journey2rich.engine.news import NewsItem


@dataclass(frozen=True)
class SignalReport:
    ticker: str
    name: str
    signal: str
    score: float
    reason: str
    price: float | None
    directional: str
    income: str


def format_report(
    reports: List[SignalReport],
    news: List[NewsItem],
    generated_at: str,
) -> str:
    lines: List[str] = []
    lines.append(f"Daily Trading Brief ({generated_at})")
    lines.append("")
    lines.append("Signals")
    for r in reports:
        price = f"${r.price:,.2f}" if r.price is not None else "n/a"
        lines.append(f"- {r.ticker} ({r.name}): {r.signal} | score {r.score:.1f} | px {price}")
        lines.append(f"  reason: {r.reason}")
        if r.directional:
            lines.append(f"  directional: {r.directional}")
        if r.income:
            lines.append(f"  income: {r.income}")

    lines.append("")
    lines.append("News Highlights")
    if not news:
        lines.append("- No matched headlines today.")
    else:
        for item in news:
            lines.append(f"- {item.title} ({item.source})")
            lines.append(f"  {item.link}")

    return "\n".join(lines)
