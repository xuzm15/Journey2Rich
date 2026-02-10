from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from journey2rich.engine.news import NewsItem
from journey2rich.engine.llm_types import LLMBrief


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
    llm: Optional[LLMBrief] = None,
) -> str:
    reason_map = {
        "score_and_trend": "基本面得分高且趋势向上",
        "weak_score_and_trend_down": "基本面较弱且趋势向下",
        "filters_not_met": "未满足过滤条件",
        "no_price_data": "缺少价格数据",
        "insufficient_history": "历史数据不足",
    }
    signal_map = {
        "BUY": "买入",
        "HOLD": "观望",
        "SELL": "卖出",
    }
    lines: List[str] = []
    lines.append(f"每日交易简报（{generated_at}）")
    lines.append("")
    lines.append("结论表")
    lines.append("| 标的 | 建议 | 评分 | 价格 | 主要原因 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for r in reports:
        price = f"${r.price:,.2f}" if r.price is not None else "n/a"
        signal = signal_map.get(r.signal, r.signal)
        reason = reason_map.get(r.reason, r.reason)
        lines.append(f"| {r.ticker}（{r.name}） | {signal} | {r.score:.1f} | {price} | {reason} |")

    lines.append("")
    lines.append("分析要点")
    for r in reports:
        if r.directional or r.income:
            lines.append(f"- {r.ticker}（{r.name}）")
            if r.directional:
                lines.append(f"  方向性：{r.directional}")
            if r.income:
                lines.append(f"  收益型：{r.income}")

    lines.append("")
    lines.append("资讯要点")
    if not news:
        lines.append("- 今日无匹配要闻。")
    else:
        for item in news:
            lines.append(f"- {item.title} ({item.source})")
            lines.append(f"  {item.link}")

    if llm:
        lines.append("")
        lines.append("模型解读（简短）")
        lines.extend([f"- {line}" for line in llm.short.splitlines() if line.strip()])
        lines.append("")
        lines.append("模型解读（详细）")
        lines.extend([f"- {line}" for line in llm.long.splitlines() if line.strip()])

    return "\n".join(lines)
