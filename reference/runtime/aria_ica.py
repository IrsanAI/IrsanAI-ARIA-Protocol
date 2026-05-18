"""Minimal viable ARIA-ICA reference implementation (deterministic local baseline)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from reference.runtime.semantic import cosine_similarity_text

ATOM_WEIGHTS = {
    "core_intent": 0.40,
    "constraints": 0.25,
    "context_dependencies": 0.15,
    "success_condition": 0.12,
    "failure_condition": 0.08,
}


@dataclass
class ICResult:
    score: float
    atoms: Dict[str, float]


def _norm_text(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _atom_score(text: str) -> float:
    # Deterministic pseudo-embedding score in [0,1] from normalized text
    if not text:
        return 0.0
    return cosine_similarity_text(text, text)


def compute_intent_checksum(atoms: Dict[str, str]) -> ICResult:
    """Computes a deterministic local IC score from the 5 semantic atoms."""
    atom_scores: Dict[str, float] = {}
    for atom, w in ATOM_WEIGHTS.items():
        atom_scores[atom] = _atom_score(_norm_text(atoms.get(atom, "")))
    total = sum(ATOM_WEIGHTS[a] * atom_scores[a] for a in ATOM_WEIGHTS)
    return ICResult(score=total, atoms=atom_scores)


def semantic_similarity(source_atoms: Dict[str, str], received_atoms: Dict[str, str]) -> float:
    weighted = 0.0
    for atom, w in ATOM_WEIGHTS.items():
        weighted += w * cosine_similarity_text(source_atoms.get(atom, ""), received_atoms.get(atom, ""))
    return max(0.0, min(1.0, weighted))
