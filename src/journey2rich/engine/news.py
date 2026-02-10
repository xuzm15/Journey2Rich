from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List

import feedparser


@dataclass(frozen=True)
class NewsItem:
    title: str
    link: str
    published: str
    source: str


def fetch_news(feed_urls: Iterable[str], limit: int = 30) -> List[NewsItem]:
    items: List[NewsItem] = []
    for url in feed_urls:
        parsed = feedparser.parse(url)
        source = parsed.feed.get("title", url)
        for entry in parsed.entries[:limit]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            published = entry.get("published", "") or entry.get("updated", "")
            items.append(NewsItem(title=title, link=link, published=published, source=source))
    return items


def filter_news(items: List[NewsItem], keywords: Dict[str, List[str]], limit: int = 8) -> List[NewsItem]:
    matched: List[NewsItem] = []
    seen = set()
    for item in items:
        title_l = item.title.lower()
        hit = False
        for ks in keywords.values():
            for k in ks:
                key = k.lower()
                if key and key in title_l:
                    hit = True
                    break
            if hit:
                break
        if hit:
            sig = (item.title, item.source)
            if sig not in seen:
                matched.append(item)
                seen.add(sig)
        if len(matched) >= limit:
            break
    return matched


def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"
