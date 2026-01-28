"""
Schiavinato Sharing Checksum Functions

This module implements the per-row checksums and Global Integrity Check (GIC) that are
unique to the Schiavinato Sharing scheme.
"""

from typing import List
from .field import mod_add

# Words per row constant
WORDS_PER_ROW = 3


def compute_row_checks(word_indices: List[int]) -> List[int]:
    """
    Computes the per-row checksum (sum of three words) for all word indices.
    
    For a mnemonic with N words arranged in rows of 3, computes N/3 checksums:
    checksum[i] = (word[3i] + word[3i+1] + word[3i+2]) mod 2053
    
    These row checksums provide error detection for individual rows and
    can be used to identify which specific shares are corrupt during recovery.
    
    Args:
        word_indices: List of BIP39 word indices (1-2048)
    
    Returns:
        List of row checksums in GF(2053)
    
    Examples:
        >>> # For 12-word mnemonic
        >>> compute_row_checks([1680, 1471, 217, 42, 1338, 279, 1907, 324, 468, 682, 1844, 126])
        [1315, 1659, 646, 599]
    """
    row_count = len(word_indices) // WORDS_PER_ROW
    checks = []
    
    for row in range(row_count):
        base = row * WORDS_PER_ROW
        sum_val = mod_add(
            mod_add(word_indices[base], word_indices[base + 1]),
            word_indices[base + 2]
        )
        checks.append(sum_val)
    
    return checks


def compute_global_integrity_check(word_indices: List[int]) -> int:
    """
    Calculates the Global Integrity Check (GIC) by summing all word indices mod 2053.
    
    This provides an overall integrity check that complements the per-row checksums.
    During recovery, if row checksums pass but the GIC fails,
    it indicates a more subtle corruption pattern.
    
    Args:
        word_indices: List of BIP39 word indices (1-2048)
    
    Returns:
        The Global Integrity Check (GIC) in GF(2053)
    
    Examples:
        >>> # For 12-word mnemonic
        >>> compute_global_integrity_check([1680, 1471, 217, 42, 1338, 279, 1907, 324, 468, 682, 1844, 126])
        113
    """
    result = 0
    for value in word_indices:
        result = mod_add(result, value)
    return result


def sum_polynomials(polynomials: List[List[int]]) -> List[int]:
    """
    Sums polynomial coefficients modulo 2053 to create a checksum polynomial.

    Given multiple polynomials, computes a new polynomial where each coefficient
    is the sum of corresponding coefficients from the input polynomials.

    Args:
        polynomials: List of coefficient lists to sum (all same length)

    Returns:
        Polynomial with summed coefficients.

    Raises:
        ValueError: If the input list is empty or degrees differ.
    """
    if len(polynomials) == 0:
        raise ValueError("Cannot sum zero polynomials")

    degree = len(polynomials[0])

    for idx, poly in enumerate(polynomials[1:], start=1):
        if len(poly) != degree:
            raise ValueError(
                f"Polynomial degree mismatch: expected {degree - 1} but got {len(poly) - 1} at index {idx}"
            )

    result = [0] * degree
    for poly in polynomials:
        for i in range(degree):
            result[i] = mod_add(result[i], poly[i])

    return result


def compute_row_check_polynomials(word_polynomials: List[List[int]]) -> List[List[int]]:
    """
    Computes row checksum polynomials by summing each row of 3 word polynomials.

    Evaluating these polynomials at any x yields the same value as summing
    the corresponding three word shares at x (Path A).
    """
    word_count = len(word_polynomials)
    if word_count % WORDS_PER_ROW != 0:
        raise ValueError("Word polynomials length must be divisible by WORDS_PER_ROW")

    row_polynomials: List[List[int]] = []
    for row in range(word_count // WORDS_PER_ROW):
        base = row * WORDS_PER_ROW
        row_polynomials.append(
            sum_polynomials(
                [
                    word_polynomials[base],
                    word_polynomials[base + 1],
                    word_polynomials[base + 2],
                ]
            )
        )
    return row_polynomials


def compute_global_check_polynomial(word_polynomials: List[List[int]]) -> List[int]:
    """
    Computes the Global Integrity Check (GIC) polynomial by summing all word polynomials.

    Evaluating this polynomial at any x yields the same value as summing all
    word shares at x (Path A).
    """
    return sum_polynomials(word_polynomials)

