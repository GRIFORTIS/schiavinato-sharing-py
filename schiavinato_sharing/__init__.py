"""
Schiavinato Sharing: Human-executable secret sharing for BIP39 mnemonics.

This library implements the Schiavinato Sharing scheme for splitting and recovering
BIP39 mnemonic phrases using arithmetic in GF(2053).

Basic usage:
    >>> from schiavinato_sharing import split_mnemonic, recover_mnemonic
    >>> 
    >>> # Split a mnemonic
    >>> mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    >>> shares = split_mnemonic(mnemonic, threshold=2, total_shares=3)
    >>> 
    >>> # Recover the mnemonic
    >>> result = recover_mnemonic(shares[:2], word_count=12)
    >>> if result.success:
    ...     print("Recovered:", result.mnemonic)

For more information, see the specification at:
https://github.com/GRIFORTIS/schiavinato-sharing-spec
"""

__version__ = "0.4.0"
__author__ = "GRIFORTIS"
__license__ = "MIT"

# Export main API functions
from .split import split_mnemonic
from .recover import recover_mnemonic

# Export field arithmetic (for advanced use)
from .field import (
    FIELD_PRIME,
    mod,
    mod_add,
    mod_sub,
    mod_mul,
    mod_inv,
    mod_div,
    mod_pow,
    GF2053,
)

# Export Lagrange functions (for manual recovery)
from .lagrange import (
    compute_lagrange_multipliers,
    lagrange_interpolate_at_zero
)

# Export polynomial functions (for testing/verification)
from .polynomial import (
    random_polynomial,
    evaluate_polynomial,
    get_random_field_element,
    configure_random_source,
)

# Export checksum functions (for verification)
from .checksums import (
    compute_row_checks,
    compute_global_integrity_check,
    compute_row_check_polynomials,
    compute_global_check_polynomial,
    sum_polynomials,
    WORDS_PER_ROW,
)

# Security utilities
from .security import (
    constant_time_equal,
    constant_time_string_equal,
    secure_wipe_list,
    secure_wipe_number,
)

# Mnemonic/seed helpers
from .seed import (
    generate_valid_mnemonic,
    mnemonic_to_indices,
    indices_to_mnemonic,
    parse_input,
)

# Export types
from .types import (
    Share,
    RecoveryResult
)

__all__ = [
    # Main API
    "split_mnemonic",
    "recover_mnemonic",
    # Field arithmetic
    "FIELD_PRIME",
    "mod",
    "mod_add",
    "mod_sub",
    "mod_mul",
    "mod_inv",
    "mod_div",
    "mod_pow",
    "GF2053",
    # Lagrange
    "compute_lagrange_multipliers",
    "lagrange_interpolate_at_zero",
    # Polynomials
    "random_polynomial",
    "evaluate_polynomial",
    "get_random_field_element",
    "configure_random_source",
    # Checksums
    "compute_row_checks",
    "compute_global_integrity_check",
    "compute_row_check_polynomials",
    "compute_global_check_polynomial",
    "sum_polynomials",
    "WORDS_PER_ROW",
    # Security
    "constant_time_equal",
    "constant_time_string_equal",
    "secure_wipe_list",
    "secure_wipe_number",
    # Mnemonic helpers
    "generate_valid_mnemonic",
    "mnemonic_to_indices",
    "indices_to_mnemonic",
    "parse_input",
    # Types
    "Share",
    "RecoveryResult",
    # Metadata
    "__version__",
    "__author__",
    "__license__"
]
