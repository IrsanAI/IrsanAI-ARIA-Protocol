"""Semantic scoring primitives for ARIA drift analysis."""
from __future__ import annotations

from typing import Dict

from reference.runtime.embeddings import lexical_cosine, sentence_transformers_cosine


def cosine_similarity_text(a: str, b: str, backend: str = "lexical", model: str = "all-MiniLM-L6-v2") -> float:
    """Semantic similarity in [0,1]. backend=lexical|sentence-transformers."""
    if backend == "sentence-transformers":
        try:
            return sentence_transformers_cosine(a, b, model=model)
        except RuntimeError:
            # graceful fallback for constrained environments
            return lexical_cosine(a, b)
    return lexical_cosine(a, b)


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
