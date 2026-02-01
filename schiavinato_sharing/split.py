"""
Schiavinato Sharing - Split Function

This module implements the share generation (splitting) logic for
Schiavinato Sharing over GF(2053).
"""

from mnemonic import Mnemonic

from .checksums import (
    WORDS_PER_ROW,
    compute_global_check_polynomial,
    compute_row_check_polynomials,
)
from .field import FIELD_PRIME, mod_add
from .polynomial import evaluate_polynomial, random_polynomial
from .security import secure_wipe_list
from .seed import validate_bip39_mnemonic
from .types import Share


def sanitize_mnemonic(mnemonic: str) -> str:
    """Normalize mnemonic by trimming and collapsing whitespace."""
    return " ".join(mnemonic.strip().lower().split())


def split_mnemonic(
    mnemonic: str,
    k: int,
    n: int,
    wordlist: list[str] | None = None,
) -> list[Share]:
    """
    Splits a BIP39 mnemonic into n Shamir shares with threshold k.

    Implements the Schiavinato Sharing scheme:
    1. Validates the BIP39 mnemonic
    2. Converts words to indices (1-2048, 1-based BIP39 indexing)
    3. Creates degree-(k-1) polynomials for word secrets
    4. Evaluates word polynomials at x = 1, 2, ..., n
    5. Computes checksum shares using dual-path validation:
       - Path A: Sum of word shares (mod 2053) - direct computation
       - Path B: Polynomial-based - sum polynomial coefficients, then evaluate

    v0.4.0 Change: Implements dual-path checksum validation to detect bit flips
    and hardware faults. Checksum polynomials are created by summing word polynomial
    coefficients, then evaluated at each share point. Both paths must agree, providing
    redundant validation that catches corruption during share generation.

    v0.3.0 Change: Checksum shares are now computed deterministically during share
    generation, enabling integrity validation during manual splitting. Row checksum
    share = sum of 3 word shares in that row. Global Integrity Check (GIC) share = sum of all
    word shares. This maintains all LSSS security properties while adding verifiability.

    Args:
        mnemonic: The BIP39 mnemonic phrase to split
        k: Threshold: number of shares required for recovery (minimum 2)
        n: Total number of shares to generate
        wordlist: Optional custom wordlist (defaults to English)

    Returns:
        List of n share objects

    Raises:
        ValueError: If inputs are invalid or mnemonic fails validation

    Examples:
        >>> shares = split_mnemonic(
        ...     'abandon abandon abandon abandon abandon abandon abandon abandon '
        ...     'abandon abandon abandon about',
        ...     2,  # 2-of-n
        ...     3   # 3 total shares
        ... )
        >>> len(shares)
        3
        >>> shares[0].share_number
        1
    """
    # Validate parameters
    if not isinstance(k, int) or not isinstance(n, int):
        raise ValueError("Threshold (k) and total shares (n) must be integers.")

    if k < 2:
        raise ValueError("Threshold k must be at least 2.")

    if k > n:
        raise ValueError("Threshold k cannot exceed n.")

    if n >= FIELD_PRIME:
        raise ValueError("Total shares (n) must be less than 2053.")

    # Normalize and validate mnemonic
    normalized_mnemonic = sanitize_mnemonic(mnemonic)

    # Get default English wordlist if none provided
    if wordlist is None:
        mnemo = Mnemonic("english")
        wordlist = mnemo.wordlist

    # Constant-time BIP39 checksum validation (JS v0.4.1 parity)
    if not validate_bip39_mnemonic(normalized_mnemonic, wordlist=wordlist):
        raise ValueError("Invalid BIP39 mnemonic: checksum verification failed.")

    # Split into words
    words = normalized_mnemonic.split(" ")
    word_count = len(words)

    if word_count not in [12, 24]:
        raise ValueError(f"Unsupported word count: {word_count}. Must be 12 or 24.")

    # Convert words to indices (1-based BIP39 indices)
    word_indices = []
    for word in words:
        try:
            index = wordlist.index(word)
            # Convert from 0-based array index to 1-based BIP39 index
            word_indices.append(index + 1)
        except ValueError as err:
            raise ValueError(f'Unknown mnemonic word: "{word}".') from err

    # Create polynomials (degree = k - 1)
    degree = k - 1

    word_polynomials = [random_polynomial(secret, degree) for secret in word_indices]

    # v0.4.0 Path B: checksum polynomials derived from word polynomials
    row_check_polynomials = compute_row_check_polynomials(word_polynomials)
    global_check_polynomial = compute_global_check_polynomial(word_polynomials)

    # Generate shares by evaluating polynomials at x = 1, 2, ..., n
    shares = []

    for share_index in range(1, n + 1):
        word_shares = [evaluate_polynomial(poly, share_index) for poly in word_polynomials]

        # v0.4.0 Dual-path checksum computation
        # Path A: direct sum of word shares
        # Path B: evaluate checksum polynomials; both must agree

        # Calculate row checksum shares using both paths
        row_count = len(word_indices) // WORDS_PER_ROW
        checksum_shares_list = []
        for row in range(row_count):
            base = row * WORDS_PER_ROW
            checksum_path_a = mod_add(
                mod_add(word_shares[base], word_shares[base + 1]),
                word_shares[base + 2],
            )
            checksum_path_b = evaluate_polynomial(row_check_polynomials[row], share_index)

            if checksum_path_a != checksum_path_b:
                raise ValueError(
                    f"Row checksum path mismatch at share {share_index}, row {row + 1}: "
                    f"Path A={checksum_path_a}, Path B={checksum_path_b}"
                )

            checksum_shares_list.append(checksum_path_a)

        # Calculate Global Integrity Check (GIC) share using both paths
        global_integrity_check_share_path_a = sum(word_shares) % FIELD_PRIME
        global_integrity_check_share_path_b = evaluate_polynomial(
            global_check_polynomial, share_index
        )

        if global_integrity_check_share_path_a != global_integrity_check_share_path_b:
            raise ValueError(
                f"Global Integrity Check (GIC) path mismatch at share {share_index}: "
                f"Path A={global_integrity_check_share_path_a}, "
                f"Path B={global_integrity_check_share_path_b}"
            )

        # Bind GIC to share number (ensures share number is embedded in validation)
        bound_gic = (global_integrity_check_share_path_a + share_index) % FIELD_PRIME

        share = Share(
            share_number=share_index,
            word_shares=word_shares,
            checksum_shares=checksum_shares_list,
            global_integrity_check_share=bound_gic,
        )
        shares.append(share)

    # Best-effort wipe sensitive data
    secure_wipe_list(word_indices)
    for poly in word_polynomials:
        secure_wipe_list(poly)
    for poly in row_check_polynomials:
        secure_wipe_list(poly)
    secure_wipe_list(global_check_polynomial)

    return shares
