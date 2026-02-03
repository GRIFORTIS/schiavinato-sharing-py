# Testing Guide (Python)

This document explains how to run the Python library tests locally and how conformance is validated.

---

## Quick start

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -e ".[dev]"
pytest
```

---

## Full local check (CI parity)

```bash
ruff check .
black --check .
mypy schiavinato_sharing
pytest
```

---

## Conformance validation (canonical test vectors)

Conformance is defined by the canonical vectors in the specification repo:
- https://github.com/GRIFORTIS/schiavinato-sharing/blob/main/test_vectors/README.md

When changing behavior, update tests so the implementation remains compatible with the vectors version it claims to support.

---

## Troubleshooting

### Environment issues

- Ensure you are in an activated virtualenv (`which python` should point to `venv/`).
- If type-checking fails, confirm you installed dev dependencies: `pip install -e ".[dev]"`.

