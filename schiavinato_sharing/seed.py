"""
Mnemonic utilities mirroring the JS helper surface.
"""

from typing import List, Tuple
from mnemonic import Mnemonic


def generate_valid_mnemonic(word_count: int) -> str:
    if word_count not in (12, 24):
        raise ValueError("Word count must be 12 or 24")
    strength = 128 if word_count == 12 else 256
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=strength)


def mnemonic_to_indices(mnemonic: str, wordlist: List[str] | None = None) -> List[int]:
    if wordlist is None:
        mnemo = Mnemonic("english")
        wordlist = mnemo.wordlist
    words = mnemonic.strip().lower().split()
    indices: List[int] = []
    for idx, word in enumerate(words):
        try:
            word_index = wordlist.index(word)
        except ValueError:
            raise ValueError(f'Word "{word}" at position {idx + 1} is not in the BIP39 wordlist')
        # Convert from 0-based array index to 1-based BIP39 index
        indices.append(word_index + 1)
    return indices


def indices_to_mnemonic(indices: List[int], wordlist: List[str] | None = None) -> str:
    if wordlist is None:
        mnemo = Mnemonic("english")
        wordlist = mnemo.wordlist
    words: List[str] = []
    for pos, index in enumerate(indices, start=1):
        if index < 1 or index > len(wordlist):
            raise ValueError(f"Index {index} at position {pos} is out of range (1-{len(wordlist)})")
        # Convert from 1-based BIP39 index to 0-based array index
        words.append(wordlist[index - 1])
    return " ".join(words)


def parse_input(input_text: str, wordlist: List[str] | None = None) -> Tuple[List[str], List[int], str]:
    """
    Parse input containing words or indices. Returns (words, indices, type).
    type is 'words', 'indices', or 'mixed'.
    """
    if wordlist is None:
        mnemo = Mnemonic("english")
        wordlist = mnemo.wordlist

    tokens = (
        input_text.strip()
        .lower()
        .replace(",", " ")
        .replace("\n", " ")
        .split()
    )

    words: List[str] = []
    indices: List[int] = []
    has_words = False
    has_indices = False

    for token in tokens:
        if token.isdigit():
            index = int(token, 10)
            if 1 <= index <= 2048:
                indices.append(index)
                # Convert from 1-based BIP39 index to 0-based array index
                words.append(wordlist[index - 1])
                has_indices = True
            else:
                raise ValueError(f"Index {index} is out of range (1-2048)")
        else:
            try:
                word_index = wordlist.index(token)
            except ValueError:
                raise ValueError(f'Word "{token}" is not in the BIP39 wordlist')
            words.append(token)
            # Convert from 0-based array index to 1-based BIP39 index
            indices.append(word_index + 1)
            has_words = True

    kind = "mixed" if has_words and has_indices else ("indices" if has_indices else "words")
    return words, indices, kind
