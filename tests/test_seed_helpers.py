import pytest

from schiavinato_sharing import (
    generate_valid_mnemonic,
    mnemonic_to_indices,
    indices_to_mnemonic,
    parse_input,
)


def test_mnemonic_index_roundtrip():
    mnemonic = generate_valid_mnemonic(12)
    indices = mnemonic_to_indices(mnemonic)
    rebuilt = indices_to_mnemonic(indices)
    assert rebuilt == mnemonic


def test_parse_input_words_indices_and_mixed():
    words, indices, kind = parse_input("abandon abandon abandon")
    assert kind == "words"
    assert indices == [1, 1, 1]

    words, indices, kind = parse_input("1 2 3")
    assert kind == "indices"
    assert words[0] == "abandon"
    assert indices[:3] == [1, 2, 3]

    words, indices, kind = parse_input("1 abandon 2")
    assert kind == "mixed"
    assert indices[0] == 1 and words[1] == "abandon"


def test_parse_input_rejects_unknown_or_out_of_range():
    with pytest.raises(ValueError):
        parse_input("notaword")
    with pytest.raises(ValueError):
        parse_input("3000")  # out of range (valid range is 1-2048)
    with pytest.raises(ValueError):
        parse_input("0")  # 0 is no longer valid (1-based indexing)
