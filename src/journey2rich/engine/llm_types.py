from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMBrief:
    short: str
    long: str
