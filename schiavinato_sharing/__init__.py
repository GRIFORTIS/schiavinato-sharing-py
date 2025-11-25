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
    >>> recovered = recover_mnemonic(shares[:2])
    >>> assert recovered == mnemonic

For more information, see the specification at:
https://github.com/GRIFORTIS/schiavinato-sharing-spec
"""

__version__ = "0.0.1"
__author__ = "GRIFORTIS"
__license__ = "MIT"

# NOTE: This is a work-in-progress implementation.
# The following imports will be uncommented as the implementation progresses.

# from .split import split_mnemonic
# from .recover import recover_mnemonic
# from .field import GF2053
# from .polynomial import Polynomial
# from .checksums import verify_checksum, generate_checksum

# __all__ = [
#     "split_mnemonic",
#     "recover_mnemonic",
#     "GF2053",
#     "Polynomial",
#     "verify_checksum",
#     "generate_checksum",
# ]

__all__ = ["__version__", "__author__", "__license__"]

