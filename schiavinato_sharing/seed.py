"""
Mnemonic utilities mirroring the JS helper surface.

Indexing policy:
- BIP39 wordlist positions are **0-based** (0..2047).
- Schiavinato Sharing math uses **1-based** word indices (1..2048) as secrets in GF(2053).
  Any +1/-1 conversion must happen ONLY at the BIP39 <-> Schiavinato boundary.
"""

import hashlib
from typing import Optional

from mnemonic import Mnemonic

from .security import constant_time_string_equal


def generate_valid_mnemonic(word_count: int) -> str:
    if word_count not in (12, 24):
        raise ValueError("Word count must be 12 or 24")
    strength = 128 if word_count == 12 else 256
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=strength)


def mnemonic_to_indices(mnemonic: str, wordlist: Optional[list[str]] = None) -> list[int]:
    if wordlist is None:
        mnemo = Mnemonic("english")
        wordlist = mnemo.wordlist
    words = mnemonic.strip().lower().split()
    indices: list[int] = []
    for idx, word in enumerate(words):
        try:
            word_index = wordlist.index(word)
        except ValueError as err:
            raise ValueError(
                f'Word "{word}" at position {idx + 1} is not in the BIP39 wordlist'
            ) from err
        # Convert from BIP39 0-based wordlist position to Schiavinato 1-based index
        indices.append(word_index + 1)
    return indices


def indices_to_mnemonic(indices: list[int], wordlist: Optional[list[str]] = None) -> str:
    if wordlist is None:
        mnemo = Mnemonic("english")
        wordlist = mnemo.wordlist
    words: list[str] = []
    for pos, index in enumerate(indices, start=1):
        if index < 1 or index > len(wordlist):
            raise ValueError(f"Index {index} at position {pos} is out of range (1-{len(wordlist)})")
        # Convert from Schiavinato 1-based index to BIP39 0-based wordlist position
        words.append(wordlist[index - 1])
    return " ".join(words)


def parse_input(
    input_text: str, wordlist: Optional[list[str]] = None
) -> tuple[list[str], list[int], str]:
    """
    Parse input containing words or indices. Returns (words, indices, type).
    type is 'words', 'indices', or 'mixed'.
    """
    if wordlist is None:
        mnemo = Mnemonic("english")
        wordlist = mnemo.wordlist

    tokens = input_text.strip().lower().replace(",", " ").replace("\n", " ").split()

    words: list[str] = []
    indices: list[int] = []
    has_words = False
    has_indices = False

    for token in tokens:
        if token.isdigit():
            index = int(token, 10)
            if 1 <= index <= 2048:
                indices.append(index)
                # Convert from Schiavinato 1-based index to BIP39 0-based wordlist position
                words.append(wordlist[index - 1])
                has_indices = True
            else:
                raise ValueError(f"Index {index} is out of range (1-2048)")
        else:
            try:
                word_index = wordlist.index(token)
            except ValueError as err:
                raise ValueError(f'Word "{token}" is not in the BIP39 wordlist') from err
            words.append(token)
            # Convert from BIP39 0-based wordlist position to Schiavinato 1-based index
            indices.append(word_index + 1)
            has_words = True

    kind = "mixed" if has_words and has_indices else ("indices" if has_indices else "words")
    return words, indices, kind


def validate_bip39_mnemonic(mnemonic: str, wordlist: Optional[list[str]] = None) -> bool:
    """
    Native BIP39 mnemonic checksum validation (constant-time checksum compare).

    Matches the canonical HTML reference approach:
    - Convert words to 0-based indices
    - Build 11-bit stream
    - Split into entropy + checksum bits
    - checksum = first (wordCount/3) bits of SHA-256(entropy)
    - Compare derived checksum bits to provided checksum bits using constant-time compare

    Notes:
    - This validates BIP39 checksum only; it does not enforce Schiavinato Sharing constraints.
    - Word indices for bit manipulation are 0-based per the BIP39 specification.
    """
    if not isinstance(mnemonic, str):
        return False

    words = mnemonic.strip().lower().split()
    word_count = len(words)

    # BIP39 allows 12/15/18/21/24 words. We keep the generic bounds for correctness.
    if word_count % 3 != 0 or word_count < 12 or word_count > 24:
        return False

    if wordlist is None:
        mnemo = Mnemonic("english")
        wordlist = mnemo.wordlist

    try:
        # 0-based indices for BIP39 bit encoding
        indices_0_based = [wordlist.index(word) for word in words]
    except ValueError:
        return False

    binary_mnemonic = "".join(f"{idx:011b}" for idx in indices_0_based)
    checksum_length = word_count // 3
    entropy_bits = (word_count * 11) - checksum_length

    entropy_binary = binary_mnemonic[:entropy_bits]
    checksum_binary = binary_mnemonic[entropy_bits:]

    # Convert entropy bits to bytes
    if entropy_bits % 8 != 0:
        # Should never happen for valid BIP39 lengths.
        return False
    entropy_bytes = bytes(int(entropy_binary[i : i + 8], 2) for i in range(0, entropy_bits, 8))

    hash_bytes = hashlib.sha256(entropy_bytes).digest()
    hash_binary = "".join(f"{b:08b}" for b in hash_bytes)
    derived_checksum = hash_binary[:checksum_length]

    return constant_time_string_equal(derived_checksum, checksum_binary)
