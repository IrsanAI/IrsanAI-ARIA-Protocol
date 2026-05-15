"""Semantic scoring primitives for ARIA drift analysis."""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Dict

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def _tokenize(text: str) -> Counter:
    return Counter(TOKEN_RE.findall(text.lower()))


def cosine_similarity_text(a: str, b: str) -> float:
    """Deterministic bag-of-words cosine similarity in [0, 1]."""
    va, vb = _tokenize(a), _tokenize(b)
    if not va and not vb:
        return 1.0
    if not va or not vb:
        return 0.0

    dot = sum(va[k] * vb.get(k, 0) for k in va)
    norm_a = math.sqrt(sum(v * v for v in va.values()))
    norm_b = math.sqrt(sum(v * v for v in vb.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (norm_a * norm_b)))


def per_atom_drift_score(source_atoms: Dict[str, str], received_atoms: Dict[str, str]) -> Dict[str, float]:
    """Returns per-atom drift (1 - similarity) for ARIA's 5 semantic atoms."""
    atoms = [
        "core_intent",
        "constraints",
        "context_dependencies",
        "success_condition",
        "failure_condition",
    ]
    result: Dict[str, float] = {}
    for atom in atoms:
        s = source_atoms.get(atom, "")
        r = received_atoms.get(atom, "")
        sim = cosine_similarity_text(s, r)
        result[atom] = 1.0 - sim
    return result
