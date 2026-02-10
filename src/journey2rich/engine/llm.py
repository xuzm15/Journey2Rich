from __future__ import annotations

import json
from typing import Dict, List, Optional

from openai import OpenAI

from journey2rich.config import get_settings
from journey2rich.engine.news import NewsItem
from journey2rich.engine.report import SignalReport
from journey2rich.engine.llm_types import LLMBrief


def _build_payload(reports: List[SignalReport], news: List[NewsItem]) -> Dict:
    return {
        "signals": [
            {
                "ticker": r.ticker,
                "name": r.name,
                "signal": r.signal,
                "score": r.score,
                "reason": r.reason,
                "price": r.price,
                "directional": r.directional,
                "income": r.income,
            }
            for r in reports
        ],
        "news": [
            {
                "title": n.title,
                "source": n.source,
                "published": n.published,
                "link": n.link,
            }
            for n in news
        ],
    }


def generate_llm_brief(reports: List[SignalReport], news: List[NewsItem]) -> Optional[LLMBrief]:
    settings = get_settings()
    if not settings.openai_api_key:
        return None

    client = OpenAI(api_key=settings.openai_api_key)
    payload = _build_payload(reports, news)

    prompt = (
        "你是专业投研助理。基于给定的结构化信号和新闻，输出两段中文分析：\n"
        "1) 简短结论：不超过6行，突出整体风险与机会。\n"
        "2) 详细分析：分点说明关键因子、风险提示、期权建议的适用前提。\n"
        "不要编造数据。不要给出确定性收益承诺。\n\n"
        f"数据：{json.dumps(payload, ensure_ascii=False)}"
    )

    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
    )

    text = response.output_text.strip()
    if not text:
        return None

    # 简单分割：若模型未分段，保底全放长文
    short = ""
    long = text
    if "详细" in text and "简短" in text:
        short = text
        long = text
    else:
        lines = text.splitlines()
        short = "\n".join(lines[:6]).strip()
        long = text

    return LLMBrief(short=short, long=long)
