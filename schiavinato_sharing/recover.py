"""
Schiavinato Sharing - Recovery Function

This module implements the share recovery (reconstruction) logic for
Schiavinato Sharing over GF(2053).
"""

from typing import List, Optional
from mnemonic import Mnemonic
from .field import mod, FIELD_PRIME
from .lagrange import lagrange_interpolate_at_zero
from .checksums import compute_row_checks, compute_global_integrity_check, WORDS_PER_ROW
from .security import constant_time_equal, secure_wipe_list, secure_wipe_number
from .types import Share, RecoveryResult


def _normalize_share_value(value: int, label: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{label} must be an integer inside GF(2053).")
    if value < 0 or value >= FIELD_PRIME:
        raise ValueError(f"{label} must be between 0 and {FIELD_PRIME - 1}.")
    return value


def recover_mnemonic(
    shares: List[Share],
    word_count: int,
    wordlist: Optional[List[str]] = None,
    strict_validation: bool = True
) -> RecoveryResult:
    """
    Performs unified recovery and validation of a mnemonic from shares.
    
    This function does not raise exceptions on validation failures; instead, it returns
    a detailed report object containing the recovered mnemonic (if successful)
    and a breakdown of any errors encountered.
    
    Recovery process:
    1. Validates share structure and uniqueness
    2. Uses Lagrange interpolation to recover word indices
    3. Uses Lagrange interpolation to recover checksums
    4. Validates row checksums
    5. Validates Global Integrity Check (GIC)
    6. Validates BIP39 checksum (if previous checks pass)
    
    Args:
        shares: List of share objects (minimum 2, typically k shares)
        word_count: Expected word count of original mnemonic (12 or 24)
        wordlist: Optional custom wordlist (defaults to English)
        strict_validation: If True, strictly validate BIP39 checksum (default: True)
    
    Returns:
        Recovery report with mnemonic and error details
    
    Examples:
        >>> result = recover_mnemonic(shares[:2], 12)
        >>> if result.success:
        ...     print('Recovered:', result.mnemonic)
        ... else:
        ...     print('Errors:', result.errors)
    """
    # Initialize mnemonic helper
    mnemo = Mnemonic('english')
    if wordlist is None:
        wordlist = mnemo.wordlist
    
    report = RecoveryResult()
    report.errors["rowPathMismatch"] = []
    report.errors["globalPathMismatch"] = False
    recovered_words: List[int] = []
    recovered_checks: List[int] = []
    recovered_global_integrity_check: int = 0
    
    try:
        # 1. Pre-flight checks for input validity
        if not shares or len(shares) < 2:
            report.errors['generic'] = 'At least two shares are required for recovery.'
            return report
        
        if word_count not in [12, 24]:
            report.errors['generic'] = f'Unsupported word count: {word_count}. Must be 12 or 24.'
            return report
        
        if word_count % WORDS_PER_ROW != 0:
            report.errors['generic'] = 'Word count must be divisible by 3.'
            return report
        
        # Validate share structure and distinctness
        row_count = word_count // WORDS_PER_ROW
        share_numbers = []
        for i, share in enumerate(shares):
            if not hasattr(share, "share_number"):
                report.errors["generic"] = f"Share {i+1} missing share_number field."
                return report

            share_numbers.append(share.share_number)

            if len(share.word_shares) != word_count:
                report.errors["generic"] = (
                    f"Share {share.share_number} has {len(share.word_shares)} "
                    f"word shares, expected {word_count}."
                )
                return report

            if len(share.checksum_shares) != row_count:
                report.errors["generic"] = (
                    f"Share {share.share_number} has {len(share.checksum_shares)} "
                    f"checksum shares, expected {row_count}."
                )
                return report

        if len(share_numbers) != len(set(share_numbers)):
            report.errors["generic"] = "Share numbers must be unique."
            return report
        
        # 2. Recover all secret numbers via Lagrange Interpolation
        for i in range(word_count):
            points = [
                (
                    mod(share.share_number),
                    _normalize_share_value(
                        share.word_shares[i],
                        f"Word share #{i + 1} (share {share.share_number})",
                    ),
                )
                for share in shares
            ]
            recovered_words.append(lagrange_interpolate_at_zero(points))

        for row in range(row_count):
            points = [
                (
                    mod(share.share_number),
                    _normalize_share_value(
                        share.checksum_shares[row],
                        f"Checksum share C{row + 1} (share {share.share_number})",
                    ),
                )
                for share in shares
            ]
            recovered_checks.append(lagrange_interpolate_at_zero(points))

        global_integrity_check_points = [
            (
                mod(share.share_number),
                _normalize_share_value(
                    share.global_integrity_check_share,
                    f"Global Integrity Check (GIC) verification (share {share.share_number})",
                ),
            )
            for share in shares
        ]
        recovered_global_integrity_check = lagrange_interpolate_at_zero(global_integrity_check_points)

        # 3. Perform internal Schiavinato validations with dual-path checking
        recomputed_checks = compute_row_checks(recovered_words)

        for row in range(row_count):
            if not constant_time_equal(recovered_checks[row], recomputed_checks[row]):
                report.errors["rowPathMismatch"].append(row)
                report.errors["row"].append(row)

        recomputed_global_integrity_check = compute_global_integrity_check(recovered_words)

        if not constant_time_equal(recovered_global_integrity_check, recomputed_global_integrity_check):
            report.errors["globalPathMismatch"] = True
            report.errors["global"] = True
        
        # 4. Convert indices to words (1-based to 0-based array index)
        try:
            # Check if indices are in valid BIP39 range (1-2048)
            for i, idx in enumerate(recovered_words):
                if idx < 1 or idx > 2048:
                    report.errors['generic'] = (
                        f'Recovered word #{i + 1} ("{idx}") is outside the BIP39 range (1–2048). '
                        f'Cannot form a valid mnemonic.'
                    )
                    return report
            
            # Convert from 1-based BIP39 indices to 0-based array indices
            recovered_word_list = [wordlist[idx - 1] for idx in recovered_words]
            recovered_mnemonic = ' '.join(recovered_word_list)
        except IndexError as e:
            report.errors['generic'] = f'Invalid word index recovered: {e}'
            return report
        
        # 5. BIP39 checksum validation
        if strict_validation:
            if not mnemo.check(recovered_mnemonic):
                report.errors['bip39'] = True
        
        # 6. Determine success
        has_errors = (
            len(report.errors['row']) > 0 or
            report.errors['global'] or
            report.errors['bip39'] or
            report.errors['generic'] is not None
        )
        
        if not has_errors:
            report.mnemonic = recovered_mnemonic
            report.success = True
        else:
            # Still return mnemonic even if there are errors (for debugging)
            report.mnemonic = recovered_mnemonic

        return report

    except Exception as e:
        report.errors['generic'] = f'Unexpected error during recovery: {str(e)}'
        return report
    finally:
        secure_wipe_list(recovered_words)
        secure_wipe_list(recovered_checks)
        recovered_global_integrity_check = secure_wipe_number(recovered_global_integrity_check)

