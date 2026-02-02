# Contributing

This repository is the Python implementation of **Schiavinato Sharing**.

The canonical protocol/spec wording lives in [`schiavinato-sharing`](https://github.com/GRIFORTIS/schiavinato-sharing). This repo focuses on a correct, testable implementation and developer tooling.

## Security status (read first)

This project is **experimental** and **not audited**. Do not use for real funds.

For the canonical security posture and reporting process, see:
- https://github.com/GRIFORTIS/schiavinato-sharing/blob/main/SECURITY.md

## Development setup

Requirements:
- Python 3.10+
- pip (latest)

```bash
git clone https://github.com/GRIFORTIS/schiavinato-sharing-py.git
cd schiavinato-sharing-py

python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

pip install -e ".[dev]"
```

## Quality gates (must pass)

```bash
mypy schiavinato_sharing
ruff check .
black --check .
pytest
```

## Pull requests

When submitting changes:
- Keep behavior compatible with the canonical protocol semantics.
- Add/update tests for any behavior change.
- Update `CHANGELOG.md` when user-facing behavior changes.

## References

- Canonical protocol + specs: https://github.com/GRIFORTIS/schiavinato-sharing
- Test vectors: https://github.com/GRIFORTIS/schiavinato-sharing/blob/main/TEST_VECTORS.md
- JavaScript implementation: https://github.com/GRIFORTIS/schiavinato-sharing-js

