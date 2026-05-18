"""
ARIA-ICA (Intent Checksum Algorithm) - Production Edition.
Multi-backend semantic drift detection with real embeddings.

Supports:
- Lexical (fast, deterministic, no deps)
- Sentence-Transformers (local, high quality)
- OpenAI (cloud, state-of-the-art)
- Claude (cloud, reasoning-aware)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Literal
from enum import Enum
import hashlib
import json
import time
import os
from abc import ABC, abstractmethod

# ============================================================================
# EMBEDDING BACKENDS
# ============================================================================

class EmbeddingBackend(Enum):
    LEXICAL = "lexical"
    SENTENCE_TRANSFORMERS = "sentence-transformers"
    OPENAI = "openai"
    CLAUDE = "claude"


class EmbeddingProvider(ABC):
    """Abstract base for embedding providers."""
    
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Embed text to vector."""
        pass
    
    @abstractmethod
    def cosine_similarity(self, text_a: str, text_b: str) -> float:
        """Compute cosine similarity between two texts."""
        pass


class LexicalEmbedding(EmbeddingProvider):
    """Fast, deterministic, no dependencies."""
    
    def embed(self, text: str) -> List[float]:
        """Tokenize text into a sparse vector representation."""
        import re
        import math
        from collections import Counter
        
        tokens = Counter(re.findall(r"[a-zA-Z0-9_]+", (text or "").lower()))
        # Convert to dense vector (top 100 tokens)
        sorted_tokens = sorted(tokens.items(), key=lambda x: x[1], reverse=True)[:100]
        return [count for _, count in sorted_tokens]
    
    def cosine_similarity(self, text_a: str, text_b: str) -> float:
        """Compute cosine similarity using lexical vectors."""
        import re
        import math
        from collections import Counter
        
        def tokenize(text: str) -> Counter:
            return Counter(re.findall(r"[a-zA-Z0-9_]+", (text or "").lower()))
        
        va, vb = tokenize(text_a), tokenize(text_b)
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


class SentenceTransformersEmbedding(EmbeddingProvider):
    """Local, high-quality embeddings using sentence-transformers."""
    
    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise RuntimeError(
                "sentence-transformers not installed. Install with: "
                "pip install sentence-transformers"
            )
        self.model = SentenceTransformer(model)
    
    def embed(self, text: str) -> List[float]:
        """Embed text using sentence-transformers."""
        return self.model.encode(text, normalize_embeddings=True).tolist()
    
    def cosine_similarity(self, text_a: str, text_b: str) -> float:
        """Compute cosine similarity."""
        import numpy as np
        va = self.model.encode(text_a, normalize_embeddings=True)
        vb = self.model.encode(text_b, normalize_embeddings=True)
        return float(np.dot(va, vb))


class OpenAIEmbedding(EmbeddingProvider):
    """Cloud-based embeddings using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        try:
            import openai
        except ImportError:
            raise RuntimeError("openai not installed. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
    
    def embed(self, text: str) -> List[float]:
        """Embed text using OpenAI."""
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding
    
    def cosine_similarity(self, text_a: str, text_b: str) -> float:
        """Compute cosine similarity."""
        import numpy as np
        va = np.array(self.embed(text_a))
        vb = np.array(self.embed(text_b))
        return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb)))


class ClaudeEmbedding(EmbeddingProvider):
    """Cloud-based embeddings using Anthropic Claude."""
    
    def __init__(self, api_key: Optional[str] = None):
        try:
            import anthropic
        except ImportError:
            raise RuntimeError("anthropic not installed. Install with: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def embed(self, text: str) -> List[float]:
        """Embed text using Claude (via API reasoning)."""
        # Claude doesn't have native embeddings, so we use a proxy approach
        # In production, use a dedicated embedding service
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": f"Summarize the semantic meaning of this text in 10 words: {text}"
            }]
        )
        summary = response.content[0].text
        # Use lexical embedding on the summary
        lexical = LexicalEmbedding()
        return lexical.embed(summary)
    
    def cosine_similarity(self, text_a: str, text_b: str) -> float:
        """Compute cosine similarity using Claude-enhanced embeddings."""
        import numpy as np
        va = np.array(self.embed(text_a))
        vb = np.array(self.embed(text_b))
        if len(va) == 0 or len(vb) == 0:
            return 0.0
        return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-10))


# ============================================================================
# INTENT CHECKSUM ALGORITHM
# ============================================================================

ATOM_WEIGHTS = {
    "core_intent": 0.40,
    "constraints": 0.25,
    "context_dependencies": 0.15,
    "success_condition": 0.12,
    "failure_condition": 0.08,
}


@dataclass
class ICResult:
    """Result of Intent Checksum computation."""
    score: float
    atoms: Dict[str, float]
    checksum: str
    backend: str
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "atoms": self.atoms,
            "checksum": self.checksum,
            "backend": self.backend,
            "timestamp": self.timestamp,
        }


class ProductionICA:
    """Production-ready Intent Checksum Algorithm with multi-backend support."""
    
    def __init__(
        self,
        backend: EmbeddingBackend = EmbeddingBackend.LEXICAL,
        **backend_kwargs
    ):
        self.backend_type = backend
        self.provider = self._init_provider(backend, **backend_kwargs)
    
    def _init_provider(
        self,
        backend: EmbeddingBackend,
        **kwargs
    ) -> EmbeddingProvider:
        """Initialize embedding provider."""
        if backend == EmbeddingBackend.LEXICAL:
            return LexicalEmbedding()
        elif backend == EmbeddingBackend.SENTENCE_TRANSFORMERS:
            model = kwargs.get("model", "all-MiniLM-L6-v2")
            return SentenceTransformersEmbedding(model=model)
        elif backend == EmbeddingBackend.OPENAI:
            api_key = kwargs.get("api_key")
            model = kwargs.get("model", "text-embedding-3-small")
            return OpenAIEmbedding(api_key=api_key, model=model)
        elif backend == EmbeddingBackend.CLAUDE:
            api_key = kwargs.get("api_key")
            return ClaudeEmbedding(api_key=api_key)
        else:
            raise ValueError(f"Unknown backend: {backend}")
    
    def compute(
        self,
        intent: str,
        constraints: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
        success_condition: Optional[str] = None,
        failure_condition: Optional[str] = None,
    ) -> ICResult:
        """Compute Intent Checksum with semantic analysis."""
        constraints = constraints or []
        context = context or {}
        success_condition = success_condition or "success"
        failure_condition = failure_condition or "failure"
        
        # Map to atoms
        atoms_text = {
            "core_intent": intent,
            "constraints": " ".join(constraints),
            "context_dependencies": json.dumps(context, sort_keys=True),
            "success_condition": success_condition,
            "failure_condition": failure_condition,
        }
        
        # Compute atom scores using embeddings
        atom_scores: Dict[str, float] = {}
        reference_text = intent  # Use intent as reference
        
        for atom, weight in ATOM_WEIGHTS.items():
            text = atoms_text.get(atom, "")
            if text:
                # Compute similarity to reference intent
                similarity = self.provider.cosine_similarity(reference_text, text)
                atom_scores[atom] = similarity
            else:
                atom_scores[atom] = 0.0
        
        # Weighted score
        total_score = sum(ATOM_WEIGHTS[a] * atom_scores[a] for a in ATOM_WEIGHTS)
        
        # Generate cryptographic checksum
        raw_payload = json.dumps({
            "score": total_score,
            "atoms": atom_scores,
            "intent_hash": hashlib.sha256(intent.encode()).hexdigest(),
            "backend": self.backend_type.value,
        }, sort_keys=True)
        checksum = hashlib.sha256(raw_payload.encode()).hexdigest()
        
        return ICResult(
            score=total_score,
            atoms=atom_scores,
            checksum=checksum,
            backend=self.backend_type.value,
        )
    
    def detect_drift(self, source_ic: ICResult, current_ic: ICResult) -> float:
        """Detect semantic drift between two Intent Checksums."""
        # If checksums match, no drift
        if source_ic.checksum == current_ic.checksum:
            return 0.0
        
        # Calculate atom-level drift
        drift = 0.0
        for atom, weight in ATOM_WEIGHTS.items():
            source_score = source_ic.atoms.get(atom, 0.0)
            current_score = current_ic.atoms.get(atom, 0.0)
            drift += weight * abs(source_score - current_score)
        
        return min(1.0, drift)  # Clamp to [0, 1]
    
    def benchmark(self, test_cases: List[tuple]) -> Dict[str, Any]:
        """Benchmark the ICA across test cases."""
        results = {
            "backend": self.backend_type.value,
            "test_cases": len(test_cases),
            "times": [],
            "drifts": [],
        }
        
        for intent_a, intent_b in test_cases:
            start = time.time()
            ic_a = self.compute(intent_a)
            ic_b = self.compute(intent_b)
            drift = self.detect_drift(ic_a, ic_b)
            elapsed = time.time() - start
            
            results["times"].append(elapsed)
            results["drifts"].append(drift)
        
        results["avg_time"] = sum(results["times"]) / len(results["times"])
        results["avg_drift"] = sum(results["drifts"]) / len(results["drifts"])
        
        return results


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def compute_ica(
    intent: str,
    backend: EmbeddingBackend = EmbeddingBackend.LEXICAL,
    **kwargs
) -> ICResult:
    """Convenience function to compute ICA."""
    ica = ProductionICA(backend=backend, **kwargs)
    return ica.compute(intent)


def detect_drift(
    intent_a: str,
    intent_b: str,
    backend: EmbeddingBackend = EmbeddingBackend.LEXICAL,
    **kwargs
) -> float:
    """Convenience function to detect drift."""
    ica = ProductionICA(backend=backend, **kwargs)
    ic_a = ica.compute(intent_a)
    ic_b = ica.compute(intent_b)
    return ica.detect_drift(ic_a, ic_b)
