from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

import requests

from journey2rich.config import get_settings
from journey2rich.data import YFinanceProvider
from journey2rich.engine.news import fetch_news, filter_news, now_iso
from journey2rich.engine.llm import generate_llm_brief
from journey2rich.engine.options import build_option_suggestions
from journey2rich.engine.report import SignalReport, format_report
from journey2rich.engine.watchlist import load_watchlist
from journey2rich.strategies.fundamental_quality import generate_signal


def _news_keywords(tickers: List[str], names: Dict[str, str]) -> Dict[str, List[str]]:
    keywords: Dict[str, List[str]] = {}
    for t in tickers:
        name = names.get(t, t)
        keywords[t] = [t.replace(".HK", ""), name]
    return keywords


def build_daily_brief() -> str:
    settings = get_settings()
    provider = YFinanceProvider()
    watchlist = load_watchlist()

    end = datetime.utcnow().date()
    start = end - timedelta(days=365 * 3)

    reports: List[SignalReport] = []
    for ticker in watchlist.tickers:
        signal = generate_signal(provider, ticker, start.isoformat(), end.isoformat())
        options = provider.get_options_chain(ticker)
        suggestions = build_option_suggestions(signal.get("price"), options, signal.get("signal"))

        reports.append(
            SignalReport(
                ticker=ticker,
                name=watchlist.names.get(ticker, ticker),
                signal=signal.get("signal", "HOLD"),
                score=float(signal.get("score", {}).get("score", 0.0)),
                reason=signal.get("reason", ""),
                price=signal.get("price"),
                directional=suggestions.get("directional", ""),
                income=suggestions.get("income", ""),
            )
        )

    feeds = [f.strip() for f in settings.news_feeds.split(",") if f.strip()]
    news_items = fetch_news(feeds)
    keywords = _news_keywords(watchlist.tickers, watchlist.names)
    matched = filter_news(news_items, keywords, limit=8)

    llm = generate_llm_brief(reports, matched)
    return format_report(reports, matched, now_iso(), llm=llm)


def push_to_discord(message: str) -> None:
    settings = get_settings()
    if not settings.discord_webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not configured")
    max_chunk = 1800
    chunks = []
    text = message
    while text:
        chunk = text[:max_chunk]
        text = text[max_chunk:]
        chunks.append(chunk)

    for chunk in chunks:
        payload = {"content": f"```\n{chunk}\n```"}
        resp = requests.post(settings.discord_webhook_url, json=payload, timeout=20)
        resp.raise_for_status()


def run_push() -> None:
    message = build_daily_brief()
    push_to_discord(message)
