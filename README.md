# schiavinato-sharing

**Python library for Schiavinato Sharing**

Human-executable secret sharing for BIP39 mnemonics using GF(2053).

[![PyPI version](https://img.shields.io/pypi/v/schiavinato-sharing.svg)](https://pypi.org/project/schiavinato-sharing/)
[![Python versions](https://img.shields.io/pypi/pyversions/schiavinato-sharing.svg)](https://pypi.org/project/schiavinato-sharing/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ⚠️ Status: Work in Progress

**This library is currently under development and not yet ready for use.**

We're working on implementing the full Schiavinato Sharing specification in Python. If you'd like to contribute or follow progress, see the [Contributing](#-contributing) section below.

### Current Status

- [ ] Core GF(2053) field arithmetic
- [ ] Polynomial operations
- [ ] Lagrange interpolation
- [ ] Mnemonic splitting
- [ ] Mnemonic recovery
- [ ] Checksum generation and validation
- [ ] Comprehensive test suite
- [ ] Documentation
- [ ] PyPI package

**Estimated availability**: Q1 2026

---

## 🎯 What is Schiavinato Sharing?

Schiavinato Sharing is a secret-sharing scheme specifically designed for **BIP39 mnemonic phrases** using **basic arithmetic in GF(2053)**. Unlike other schemes, it can be performed entirely **by hand** with pencil and paper, making it ideal for:

- 🏦 Long-term inheritance planning
- 🔐 Disaster recovery scenarios
- 🌍 Situations where digital tools are unavailable or untrusted
- 👨‍👩‍👧‍👦 Family backup strategies

---

## 📦 Installation (When Available)

```bash
pip install schiavinato-sharing
```

---

## 🚀 Quick Start (Planned API)

### Splitting a Mnemonic

```python
from schiavinato_sharing import split_mnemonic

mnemonic = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about'
threshold = 2  # Minimum shares needed to recover
total_shares = 3  # Total shares to create

shares = split_mnemonic(mnemonic, threshold, total_shares)
print(shares)
# [
#   'share 1 of 3: word1 word2 ... wordN [checksum]',
#   'share 2 of 3: word1 word2 ... wordN [checksum]',
#   'share 3 of 3: word1 word2 ... wordN [checksum]'
# ]
```

### Recovering a Mnemonic

```python
from schiavinato_sharing import recover_mnemonic

shares = [
    'share 1 of 3: word1 word2 ... wordN [checksum]',
    'share 2 of 3: word1 word2 ... wordN [checksum]'
]

recovered = recover_mnemonic(shares)
print(recovered)
# 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about'
```

---

## 📚 Documentation

### Specification

This library implements the Schiavinato Sharing specification:

🔗 **[Specification Repository](https://github.com/GRIFORTIS/schiavinato-sharing-spec)**

Key documents:
- [Whitepaper](https://github.com/GRIFORTIS/schiavinato-sharing-spec/blob/main/WHITEPAPER.md) – Complete mathematical description
- [Test Vectors](https://github.com/GRIFORTIS/schiavinato-sharing-spec/blob/main/TEST_VECTORS.md) – Validation data
- [Reference Implementation](https://github.com/GRIFORTIS/schiavinato-sharing-spec/tree/main/reference-implementation) – HTML tool

### Sister Implementation

For immediate use, see the JavaScript library:

🔗 **[JavaScript Library](https://github.com/GRIFORTIS/schiavinato-sharing-js)**

```bash
npm install @grifortis/schiavinato-sharing
```

---

## 🧪 Development

### Setup

```bash
# Clone the repository
git clone https://github.com/GRIFORTIS/schiavinato-sharing-py.git
cd schiavinato-sharing-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy schiavinato_sharing

# Linting
ruff check .

# Formatting
black .
```

### Project Structure

```
schiavinato-sharing-py/
├── schiavinato_sharing/
│   ├── __init__.py
│   ├── field.py              # GF(2053) field arithmetic
│   ├── polynomial.py         # Polynomial operations
│   ├── lagrange.py           # Lagrange interpolation
│   ├── split.py              # Mnemonic splitting
│   ├── recover.py            # Mnemonic recovery
│   ├── checksums.py          # Checksum generation/validation
│   └── utils/
│       ├── __init__.py
│       ├── validation.py     # Input validation
│       └── security.py       # Security utilities
├── tests/
│   ├── test_field.py
│   ├── test_polynomial.py
│   └── ...
├── examples/
│   └── basic_usage.py
├── setup.py
├── pyproject.toml
└── README.md
```

---

## 🤝 Contributing

We welcome contributions! This project is in early development, so there's plenty to do.

### How to Help

- 🐍 **Implement core functionality** – Help write the library!
- 🧪 **Write tests** – Ensure correctness with comprehensive tests
- 📖 **Documentation** – Improve README, docstrings, examples
- 🔍 **Review** – Check for bugs, security issues, or improvements

### Getting Started

1. **Read the spec**: [Schiavinato Sharing Whitepaper](https://github.com/GRIFORTIS/schiavinato-sharing-spec/blob/main/WHITEPAPER.md)
2. **Check test vectors**: [TEST_VECTORS.md](https://github.com/GRIFORTIS/schiavinato-sharing-spec/blob/main/TEST_VECTORS.md)
3. **Look at JS implementation**: [schiavinato-sharing-js](https://github.com/GRIFORTIS/schiavinato-sharing-js) for reference
4. **Open an issue**: Discuss your contribution before starting

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🔒 Security

### Security Status: ⚠️ EXPERIMENTAL (Not Yet Implemented)

When this library is released, it will be **experimental software** that has NOT been professionally audited.

**DO NOT USE FOR REAL FUNDS** until:
- [ ] Implementation complete
- [ ] Professional security audit
- [ ] Extensive peer review
- [ ] v1.0.0 release

See [SECURITY.md](.github/SECURITY.md) for reporting vulnerabilities.

---

## 📄 License

[MIT License](LICENSE) – see file for details.

---

## 🔗 Related Projects

- **[Specification](https://github.com/GRIFORTIS/schiavinato-sharing-spec)** – Whitepaper and reference implementation
- **[JavaScript Library](https://github.com/GRIFORTIS/schiavinato-sharing-js)** – Production-ready npm package
- **[GRIFORTIS](https://github.com/GRIFORTIS)** – Organization homepage

---

## 📬 Contact

- 📖 **Documentation**: [Specification repo](https://github.com/GRIFORTIS/schiavinato-sharing-spec)
- 🐛 **Bug Reports**: [Open an issue](https://github.com/GRIFORTIS/schiavinato-sharing-py/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/GRIFORTIS/schiavinato-sharing-py/discussions)
- 📧 **Email**: support@grifortis.com

---

## 🙏 Acknowledgments

This implementation is based on:
- Shamir, A. (1979). "How to Share a Secret"
- BIP39: Mnemonic code for generating deterministic keys
- The Schiavinato Sharing specification by Renato Schiavinato Lopez

---

**Made with ❤️ by [GRIFORTIS](https://github.com/GRIFORTIS)**

*Empowering digital sovereignty through open-source tools.*

