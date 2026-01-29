"""
Schiavinato Sharing - Type Definitions

This module defines all data classes and types used by the library.
"""

from dataclasses import dataclass, field
from typing import Optional, TypedDict, cast


@dataclass
class Share:
    """
    Represents a single Shamir share containing word shares, checksums, and the
    Global Integrity Check (GIC).
    """

    share_number: int
    """The X coordinate for this share (must be unique and non-zero)"""

    word_shares: list[int]
    """Array of word index shares (length = number of words in mnemonic)"""

    checksum_shares: list[int]
    """Array of row checksum shares (length = number of rows = wordCount / 3)"""

    global_integrity_check_share: int
    """Global Integrity Check (GIC) verification number share"""


RecoveryErrors = TypedDict(
    "RecoveryErrors",
    {
        "row": list[int],
        "global": bool,
        "bip39": bool,
        "generic": Optional[str],
        "rowPathMismatch": list[int],
        "globalPathMismatch": bool,
    },
)


@dataclass
class RecoveryResult:
    """
    Result object returned by the recovery function.
    """

    mnemonic: Optional[str] = None
    """The recovered mnemonic phrase (None if recovery failed)"""

    errors: RecoveryErrors = field(
        default_factory=lambda: cast(
            RecoveryErrors,
            {
                "row": [],
                "global": False,
                "bip39": False,
                "generic": None,
                "rowPathMismatch": [],
                "globalPathMismatch": False,
            },
        )
    )
    """Detailed error information"""

    success: bool = False
    """True if recovery was successful with no errors"""

    shares_with_invalid_checksums: set[int] = field(default_factory=set)
    """Set of share numbers that had invalid checksums (if any)"""
