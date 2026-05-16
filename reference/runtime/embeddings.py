"""Embedding backends for ARIA semantic scoring.

Backends:
- lexical (default, deterministic, no deps)
- sentence-transformers (optional, local model)
"""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import List

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def _tokenize(text: str) -> Counter:
    return Counter(TOKEN_RE.findall((text or "").lower()))


def lexical_embedding(text: str) -> Counter:
    return _tokenize(text)


def lexical_cosine(a: str, b: str) -> float:
    va, vb = lexical_embedding(a), lexical_embedding(b)
    if not va and not vb:
        return 1.0
    if not va or not vb:
        return 0.0
    dot = sum(va[k] * vb.get(k, 0) for k in va)
    na = math.sqrt(sum(v * v for v in va.values()))
    nb = math.sqrt(sum(v * v for v in vb.values()))
    if na == 0 or nb == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (na * nb)))


def _cosine_vec(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (na * nb)))


def sentence_transformers_cosine(a: str, b: str, model: str = "all-MiniLM-L6-v2") -> float:
    """Optional backend. Falls back by raising RuntimeError if dependency missing."""
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("sentence-transformers is not installed") from exc

    m = SentenceTransformer(model)
    va, vb = m.encode([a, b], normalize_embeddings=False)
    return _cosine_vec(list(va), list(vb))
