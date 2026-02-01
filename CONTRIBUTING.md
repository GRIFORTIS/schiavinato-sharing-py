# Contributing to schiavinato-sharing-py

Thank you for your interest in contributing to the Python implementation of Schiavinato Sharing!

## 📋 Current Status

**This project is implemented and tested (v0.4.1), but still experimental.**

Development goal: maintain parity with the canonical specification + reference implementation while keeping the library safe for manual-first workflows.

### Zero-Knowledge Protocol

GRIFORTIS operates under a strict zero-knowledge protocol for consultancy and professional services. This principle informs our technical design:

- **User sovereignty**: Tools must enable users to maintain exclusive control of secrets
- **No custody assumptions**: Never design features that require trusting third parties with mnemonics
- **Advisory interfaces**: Guide users through processes they execute themselves

This library implements the core cryptographic operations while maintaining these principles.

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.12 (We recommend using [pyenv](https://github.com/pyenv/pyenv) to manage versions)
- **pip**: Latest version
- **Tip**: This project includes a `.python-version` file. If you use pyenv, it will automatically switch to the correct version.
- **Git**: Latest stable version

### Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/schiavinato-sharing-py.git
cd schiavinato-sharing-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify setup
pytest
```

## 📚 Implementation Guide

### Reference Materials

Before implementing, review:

1. **[Whitepaper](https://github.com/GRIFORTIS/schiavinato-sharing-spec/releases/latest/download/WHITEPAPER.pdf)** ([LaTeX source](https://github.com/GRIFORTIS/schiavinato-sharing-spec/blob/main/WHITEPAPER.tex)) – Full specification
2. **[Test Vectors](https://github.com/GRIFORTIS/schiavinato-sharing-spec/blob/main/TEST_VECTORS.md)** – Expected outputs
3. **[JavaScript Implementation](https://github.com/GRIFORTIS/schiavinato-sharing-js)** – Reference implementation

### Implementation Roadmap

Phase 1: Core Cryptography
- [x] `field.py` – GF(2053) field arithmetic
- [x] `polynomial.py` – Polynomial operations
- [x] `lagrange.py` – Lagrange interpolation

Phase 2: Schiavinato Logic
- [x] `split.py` – Mnemonic splitting
- [x] `recover.py` – Mnemonic recovery
- [x] `checksums.py` – Checksum generation/validation

Phase 3: Utilities
- [x] `security.py` – Security utilities
- [x] `seed.py` – Mnemonic helpers and native BIP39 checksum validation

Phase 4: Testing & Documentation
- [x] Comprehensive test suite
- [ ] Documentation polish (README/API docs)
- [ ] Performance benchmarks (optional)

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=schiavinato_sharing

# Run specific test file
pytest tests/test_field.py

# Run in watch mode (requires pytest-watch)
ptw
```

### Writing Tests

```python
import pytest
from schiavinato_sharing.field import GF2053


def test_field_addition():
    """Test addition in GF(2053)."""
    field = GF2053()
    assert field.add(100, 200) == 300
    assert field.add(2000, 100) == 47  # (2000 + 100) % 2053


def test_field_addition_edge_cases():
    """Test edge cases for field addition."""
    field = GF2053()
    assert field.add(0, 0) == 0
    assert field.add(2052, 1) == 0  # (2052 + 1) % 2053
```

## 📝 Code Style

### Type Hints

All functions must have type hints:

```python
from typing import List

def split_mnemonic(
    mnemonic: str,
    k: int,
    n: int
) -> List["Share"]:
    """
    Split a BIP39 mnemonic into shares.
    
    Args:
        mnemonic: Valid BIP39 mnemonic phrase
        k: Minimum shares needed for recovery (threshold)
        n: Total shares to generate
        
    Returns:
        List of Share objects
        
    Raises:
        ValueError: If inputs are invalid
    """
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def recover_mnemonic(shares: List[str]) -> str:
    """
    Recover a BIP39 mnemonic from shares.
    
    Args:
        shares: List of share strings (at least k shares required)
        
    Returns:
        Recovered BIP39 mnemonic phrase
        
    Raises:
        ValueError: If shares are invalid
        ChecksumError: If share checksums don't match
        
    Example:
        >>> shares = [
        ...     'share 1 of 3: ...',
        ...     'share 2 of 3: ...'
        ... ]
        >>> mnemonic = recover_mnemonic(shares)
    """
    pass
```

### Formatting

We use:
- **Black** for code formatting
- **isort** for import sorting
- **Ruff** for linting
- **mypy** for type checking

```bash
# Format code
black .

# Sort imports
isort .

# Lint
ruff check .

# Type check
mypy schiavinato_sharing
```

## 🔧 Development Workflow

```bash
# Create feature branch
git checkout -b feature/field-arithmetic

# Make changes
# Edit files in schiavinato_sharing/

# Format and check
black .
isort .
ruff check .
mypy schiavinato_sharing

# Run tests
pytest

# Commit with clear message
git commit -m "feat: implement GF(2053) field arithmetic"

# Push and create PR
git push origin feature/field-arithmetic
```

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] All tests pass: `pytest`
- [ ] Type checking passes: `mypy schiavinato_sharing`
- [ ] Linting passes: `ruff check .`
- [ ] Code formatted: `black .` and `isort .`
- [ ] Docstrings added to all public functions
- [ ] Tests added for new functionality
- [ ] CHANGELOG.md updated (if applicable)

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add GF(2053) field arithmetic
fix: correct polynomial evaluation
docs: improve split_mnemonic docstring
test: add edge cases for recovery
refactor: simplify checksum validation
```

## 🎯 Areas We Need Help

### High Priority
- [ ] Implement `field.py` (GF(2053) arithmetic)
- [ ] Implement `polynomial.py`
- [ ] Implement `split.py` and `recover.py`
- [ ] Write comprehensive tests

### Medium Priority
- [ ] Add examples and tutorials
- [ ] Performance optimization
- [ ] Additional BIP39 language support

### Low Priority
- [ ] CLI tool
- [ ] Sphinx documentation
- [ ] Jupyter notebook examples

## 📖 Resources

- **Specification**: https://github.com/GRIFORTIS/schiavinato-sharing-spec
- **JS Implementation**: https://github.com/GRIFORTIS/schiavinato-sharing-js
- **Discussions**: https://github.com/GRIFORTIS/schiavinato-sharing-py/discussions

## 🐛 Reporting Issues

- **Bugs**: Use "Bug Report" template
- **Features**: Use "Feature Request" template
- **Questions**: Start a Discussion

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping build Schiavinato Sharing in Python! 🐍

