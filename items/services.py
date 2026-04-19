import re
from dataclasses import dataclass
from typing import Iterable

from .models import Item


def _tokenize(text: str) -> set[str]:
    text = (text or "").lower()
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"[^0-9a-zA-Z\u4e00-\u9fff]+", text)
    return {p for p in parts if p}


def keyword_score(a: str, b: str) -> float:
    ta = _tokenize(a)
    tb = _tokenize(b)
    if not ta or not tb:
        return 0.0
    inter = ta & tb
    union = ta | tb
    return len(inter) / max(1, len(union))


@dataclass
class MatchResult:
    item: Item
    score: float


def recommend_matches(source: Item, candidates: Iterable[Item], limit: int = 6) -> list[MatchResult]:
    results: list[MatchResult] = []
    source_text = f"{source.title} {source.description} {source.location}"

    for c in candidates:
        cand_text = f"{c.title} {c.description} {c.location}"
        score = keyword_score(source_text, cand_text)
        if score > 0:
            results.append(MatchResult(item=c, score=score))

    results.sort(key=lambda r: (r.score, r.item.created_at), reverse=True)
    return results[:limit]
