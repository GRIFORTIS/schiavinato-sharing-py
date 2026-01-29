from schiavinato_sharing import (
    configure_random_source,
    generate_valid_mnemonic,
    get_random_field_element,
    indices_to_mnemonic,
    mnemonic_to_indices,
    recover_mnemonic,
    split_mnemonic,
)

TEST_MNEMONIC = "spin result brand ahead poet carpet unusual chronic denial festival toy autumn"


def test_row_checksum_path_mismatch_detected():
    shares = split_mnemonic(TEST_MNEMONIC, 2, 3)
    # Tamper first row checksum in first share to force Path B mismatch
    shares[0].checksum_shares[0] = (shares[0].checksum_shares[0] + 1) % 2053

    result = recover_mnemonic([shares[0], shares[1]], 12)

    assert result.success is False
    assert 0 in result.errors["rowPathMismatch"]
    assert 0 in result.errors["row"]


def test_global_integrity_check_path_mismatch_detected():
    shares = split_mnemonic(TEST_MNEMONIC, 2, 3)
    shares[0].global_integrity_check_share = (shares[0].global_integrity_check_share + 1) % 2053

    result = recover_mnemonic([shares[0], shares[1]], 12)

    assert result.success is False
    assert result.errors["globalPathMismatch"] is True
    assert result.errors["global"] is True


def test_configurable_random_source_used():
    calls = 0

    def fake_random(byte_count: int) -> bytes:
        nonlocal calls
        calls += 1
        return bytes([1] * byte_count)  # value = 16843009 (for 4 bytes) < 4292877712

    configure_random_source(fake_random)
    value = get_random_field_element()

    assert calls >= 1
    assert value == 16843009 % 2053  # = 197


def test_mnemonic_index_roundtrip():
    words = TEST_MNEMONIC.split()
    indices = mnemonic_to_indices(TEST_MNEMONIC)
    rebuilt = indices_to_mnemonic(indices)
    assert words == rebuilt.split()


def test_generate_valid_mnemonic_lengths():
    mnemonic12 = generate_valid_mnemonic(12)
    assert len(mnemonic12.split()) == 12
    mnemonic24 = generate_valid_mnemonic(24)
    assert len(mnemonic24.split()) == 24


def test_path_agreement_across_thresholds_and_lengths():
    cases = [
        (12, 2, 3),
        (12, 3, 5),
        (24, 2, 3),
    ]
    for word_count, k, n in cases:
        mnemonic = generate_valid_mnemonic(word_count)
        shares = split_mnemonic(mnemonic, k, n)
        result = recover_mnemonic(shares[:k], word_count)
        assert result.success is True
        assert result.errors["rowPathMismatch"] == []
        assert result.errors["globalPathMismatch"] is False


def test_word_share_tampering_triggers_path_mismatch():
    shares = split_mnemonic(TEST_MNEMONIC, 2, 3)
    # Tamper a word share (not the checksum) to force recomputed checksum mismatch
    shares[0].word_shares[0] = (shares[0].word_shares[0] + 1) % 2053
    result = recover_mnemonic([shares[0], shares[1]], 12)
    assert result.success is False
    assert 0 in result.errors["row"]
    assert 0 in result.errors["rowPathMismatch"]
