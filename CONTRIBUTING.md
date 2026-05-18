# Contributing to ARIA Protocol

Thank you for your interest in contributing to ARIA! We're building the semantic standard for AI agents, and we need talented developers, researchers, and architects like you.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Contribution Types](#contribution-types)
5. [Pull Request Process](#pull-request-process)
6. [Coding Standards](#coding-standards)
7. [Testing](#testing)
8. [Documentation](#documentation)
9. [Community](#community)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

**In short:**
- Be respectful and constructive
- Welcome diverse perspectives
- Focus on the problem, not the person
- Report violations to conduct@aria-protocol.dev

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- GitHub account
- Basic understanding of agent systems and semantic integrity

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/IrsanAI/IrsanAI-ARIA-Protocol.git
cd IrsanAI-ARIA-Protocol

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### Verify Setup

```bash
# Run the CLI demo
python reference/runtime/cli_demo_production.py

# Expected output: "✓ ARIA Protocol architecture demonstrated successfully!"
```

---

## Development Workflow

### 1. Create an Issue

Before starting work, create an issue describing:
- **Problem:** What needs to be fixed or added?
- **Proposed Solution:** How do you plan to solve it?
- **Acceptance Criteria:** How will we know it's done?

Example:
```
Title: Add GPU acceleration for sentence-transformers backend

Description:
Currently, sentence-transformers embeddings are CPU-bound, limiting throughput.
We should add optional GPU support to improve performance.

Acceptance Criteria:
- [ ] GPU detection and initialization
- [ ] Benchmark showing 5x+ speedup on NVIDIA GPUs
- [ ] Fallback to CPU if GPU unavailable
- [ ] Documentation for setup
```

### 2. Fork & Branch

```bash
# Fork on GitHub (click the "Fork" button)

# Clone your fork
git clone https://github.com/YOUR_USERNAME/IrsanAI-ARIA-Protocol.git
cd IrsanAI-ARIA-Protocol

# Add upstream remote
git remote add upstream https://github.com/IrsanAI/IrsanAI-ARIA-Protocol.git

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation
- `test/` for tests
- `refactor/` for code improvements

### 3. Make Changes

```bash
# Make your changes
# Test frequently
pytest tests/

# Commit with clear messages
git commit -m "feat: Add GPU acceleration for embeddings"
```

**Commit message format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `ci`

### 4. Keep Updated

```bash
# Fetch latest changes
git fetch upstream

# Rebase on main
git rebase upstream/main
```

### 5. Push & Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Link to the issue: "Closes #123"
```

---

## Contribution Types

### 1. RFC Contributions

**What we're looking for:**
- New RFCs for protocol extensions
- Improvements to existing RFCs
- Security considerations
- Performance analysis

**Format:**
```markdown
# ARIA-RFC-XXX: Your Proposal Title

## Summary
Brief description of the proposal.

## Motivation
Why is this needed?

## Specification
Detailed technical specification.

## Implementation
Reference implementation details.
```

**RFC Authoring Rules:**
- Use concise section numbering
- Explicitly separate normative requirements (MUST/SHOULD/MAY) from informative examples
- Define datatypes, allowed ranges, and failure behaviors for new fields
- Ensure internal consistency across related RFCs
- Align terminology with RFC-001 and RFC-002

### 2. Code Contributions

**What we're looking for:**
- New embedding backends (Hugging Face, local models, etc.)
- Performance optimizations
- Bug fixes
- Additional RFC implementations
- Framework integrations (Langchain, Haystack, etc.)

**Example:**
```python
# reference/runtime/embeddings_gpu.py
class GPUEmbedding(EmbeddingProvider):
    """GPU-accelerated embeddings using CUDA."""
    
    def __init__(self, device: str = "cuda:0"):
        self.device = device
        # Implementation...
```

### 3. Documentation Contributions

**What we're looking for:**
- Tutorials and guides
- API documentation improvements
- Architecture diagrams
- Integration examples
- Troubleshooting guides

**Example:**
```markdown
# Getting Started with ARIA + LangGraph

This guide shows how to integrate ARIA Protocol with LangGraph...

## Step 1: Install ARIA
```

### 4. Test Contributions

**What we're looking for:**
- Unit tests for new features
- Integration tests
- Benchmark tests
- Edge case coverage

**Example:**
```python
# tests/test_aria_ica_production.py
def test_drift_detection_with_openai_backend():
    ica = ProductionICA(backend=EmbeddingBackend.OPENAI)
    ic_a = ica.compute("Buy Apple stock")
    ic_b = ica.compute("Purchase AAPL shares")
    drift = ica.detect_drift(ic_a, ic_b)
    assert 0.0 <= drift <= 1.0
```

### 5. Research Contributions

**What we're looking for:**
- Papers on semantic drift detection
- Benchmarking studies
- Comparative analysis with other protocols
- Case studies

---

## Pull Request Process

### Before Submitting

- [ ] Code follows our style guide
- [ ] All tests pass: `pytest tests/`
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts

### Submission

1. **Title:** Clear, descriptive title
   ```
   feat(embeddings): Add GPU acceleration for sentence-transformers
   ```

2. **Description:** Fill out the PR template
   ```markdown
   ## Description
   Adds GPU support to sentence-transformers backend...
   
   ## Related Issue
   Closes #123
   
   ## Changes
   - Added `GPUEmbedding` class
   - Added GPU detection logic
   - Added benchmarks
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Benchmarks show 5x+ improvement
   ```

3. **Reviewers:** Request review from maintainers

### Review Process

- **Automated Checks:** Tests, linting, coverage
- **Code Review:** 1-2 maintainers review
- **Feedback:** We'll request changes if needed
- **Approval:** Merge when approved

**Timeline:** Typically 2-5 business days

---

## Coding Standards

### Python Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these additions:

```python
# Type hints required
def compute_ica(
    intent: str,
    backend: EmbeddingBackend = EmbeddingBackend.LEXICAL,
) -> ICResult:
    """Compute Intent Checksum Algorithm.
    
    Args:
        intent: The mission intent
        backend: Embedding backend to use
        
    Returns:
        ICResult with semantic checksum
        
    Raises:
        ValueError: If backend not found
    """
    pass

# Docstrings required (Google style)
class ProductionICA:
    """Production-ready Intent Checksum Algorithm.
    
    Supports multiple embedding backends for semantic drift detection.
    """
    pass

# Constants in UPPER_CASE
ATOM_WEIGHTS = {
    "core_intent": 0.40,
    "constraints": 0.25,
}

# Private methods with leading underscore
def _compute_atom_scores(text: str) -> Dict[str, float]:
    pass
```

### Formatting

```bash
# Format code
black reference/runtime/

# Check linting
flake8 reference/runtime/

# Sort imports
isort reference/runtime/

# Type checking
mypy reference/runtime/
```

### Performance

- Lexical backend: < 1ms per operation
- Sentence-Transformers: < 10ms per operation
- Cloud backends: < 200ms per operation

---

## Testing

### Running Tests

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/test_aria_ica_production.py

# With coverage
pytest --cov=reference/runtime tests/

# Verbose output
pytest -v tests/
```

### Writing Tests

```python
# tests/test_my_feature.py
import pytest
from aria_ica_production import ProductionICA, EmbeddingBackend

class TestMyFeature:
    """Test suite for my feature."""
    
    def setup_method(self):
        """Setup before each test."""
        self.ica = ProductionICA(backend=EmbeddingBackend.LEXICAL)
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = self.ica.compute("Test intent")
        assert result.score > 0
        assert len(result.checksum) == 64  # SHA256
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            self.ica.compute("")
    
    @pytest.mark.parametrize("backend", [
        EmbeddingBackend.LEXICAL,
        EmbeddingBackend.SENTENCE_TRANSFORMERS,
    ])
    def test_multiple_backends(self, backend):
        """Test with multiple backends."""
        ica = ProductionICA(backend=backend)
        result = ica.compute("Test")
        assert result is not None
```

### Benchmarking

```python
# tests/benchmarks/test_performance.py
import pytest

@pytest.mark.benchmark
def test_ica_performance(benchmark):
    """Benchmark ICA computation."""
    ica = ProductionICA(backend=EmbeddingBackend.LEXICAL)
    result = benchmark(ica.compute, "Buy Apple stock for $10,000")
    assert result.score > 0
```

---

## Documentation

### Code Comments

```python
# Good: Explains WHY, not WHAT
# We use weighted atoms to preserve semantic context
# across agent hops, with core_intent weighted highest
atom_scores = compute_atoms(intent)

# Bad: Obvious from code
# Loop through atoms
for atom in atoms:
    pass
```

### Docstrings

```python
def detect_drift(
    source_ic: ICResult,
    current_ic: ICResult,
) -> float:
    """Detect semantic drift between two Intent Checksums.
    
    Compares the semantic integrity of two checksums by analyzing
    atom-level differences. Returns a drift score in [0, 1] where
    0 = identical and 1 = completely different.
    
    Args:
        source_ic: Original Intent Checksum
        current_ic: Current Intent Checksum
        
    Returns:
        Drift score in range [0, 1]
        
    Example:
        >>> ica = ProductionICA()
        >>> ic_a = ica.compute("Buy Apple stock")
        >>> ic_b = ica.compute("Purchase AAPL shares")
        >>> drift = ica.detect_drift(ic_a, ic_b)
        >>> print(f"Drift: {drift:.2%}")
        Drift: 5.23%
    """
```

### README Updates

When adding features, update relevant README sections:
- Installation instructions
- Quick start examples
- API reference
- Troubleshooting

---

## Community

### Getting Help

- **GitHub Discussions:** https://github.com/IrsanAI/IrsanAI-ARIA-Protocol/discussions
- **GitHub Issues:** https://github.com/IrsanAI/IrsanAI-ARIA-Protocol/issues
- **Email:** support@aria-protocol.dev

### Communication Channels

- **Discord:** [Join our community](https://discord.gg/aria-protocol)
- **Twitter:** [@ARIAProtocol](https://twitter.com/ARIAProtocol)
- **Blog:** https://aria-protocol.dev/blog

### Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Release notes
- Project website

---

## Frequently Asked Questions

### Q: How long does review take?

A: Typically 2-5 business days. Complex changes may take longer.

### Q: Can I work on multiple issues?

A: Yes! But focus on one at a time for quality.

### Q: What if my PR gets rejected?

A: No worries! We'll explain why and suggest improvements. You can always revise and resubmit.

### Q: Do I need to sign a CLA?

A: No, but by contributing you agree to license your work under the Apache 2.0 License.

### Q: How can I become a maintainer?

A: Contribute consistently, help review PRs, and engage with the community. We'll invite you when ready.

---

## Resources

- [ARIA Protocol Docs](https://aria-protocol.dev/docs)
- [RFC Process](docs/rfcs/README.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Interop Report](docs/INTEROP_REPORT_2026.md)

---

**Thank you for contributing to ARIA! Together, we're building the future of AI agent communication.** 🚀

---

*Last updated: May 17, 2026*  
*Maintained by: ARIA Core Team*
