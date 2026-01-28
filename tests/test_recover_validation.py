import pytest

from schiavinato_sharing import recover_mnemonic, split_mnemonic, FIELD_PRIME
from schiavinato_sharing.types import Share


VALID_MNEMONIC = (
    "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
)


def test_recover_rejects_unsupported_wordcount():
    shares = split_mnemonic(VALID_MNEMONIC, 2, 3)
    result = recover_mnemonic(shares, 15)
    assert result.success is False
    assert "Unsupported word count" in result.errors["generic"]


def test_recover_rejects_wrong_wordshare_length():
    share1 = Share(share_number=1, word_shares=[1, 2], checksum_shares=[3, 4], global_integrity_check_share=0)
    share2 = Share(share_number=2, word_shares=[1, 2], checksum_shares=[3, 4], global_integrity_check_share=0)
    result = recover_mnemonic([share1, share2], 12)
    assert result.success is False
    assert "word shares" in result.errors["generic"]


def test_recover_rejects_wrong_checksum_length():
    share1 = Share(share_number=1, word_shares=[0] * 12, checksum_shares=[1], global_integrity_check_share=0)
    share2 = Share(share_number=2, word_shares=[0] * 12, checksum_shares=[1], global_integrity_check_share=0)
    result = recover_mnemonic([share1, share2], 12)
    assert result.success is False
    assert "checksum shares" in result.errors["generic"]


def test_recover_rejects_duplicate_share_numbers():
    share = Share(share_number=1, word_shares=[0] * 12, checksum_shares=[0, 0, 0, 0], global_integrity_check_share=0)
    result = recover_mnemonic([share, share], 12)
    assert result.success is False
    assert "unique" in result.errors["generic"].lower()


def test_recover_rejects_out_of_range_share_value():
    share1 = Share(share_number=1, word_shares=[FIELD_PRIME] + [0] * 11, checksum_shares=[0, 0, 0, 0], global_integrity_check_share=0)
    share2 = Share(share_number=2, word_shares=[0] * 12, checksum_shares=[0, 0, 0, 0], global_integrity_check_share=0)
    result = recover_mnemonic([share1, share2], 12)
    assert result.success is False
    assert "between 0 and" in result.errors["generic"]


def test_recover_bip39_strict_flagging():
    # Make a valid recovery then force strict_validation=True to be exercised
    shares = split_mnemonic(VALID_MNEMONIC, 2, 3)
    result = recover_mnemonic([shares[0], shares[1]], 12, strict_validation=True)
    assert result.success is True


def test_recover_flags_row_path_mismatch():
    shares = split_mnemonic(VALID_MNEMONIC, 2, 3)
    base = shares[0]
    tampered_row = Share(
        share_number=base.share_number,
        word_shares=list(base.word_shares),
        checksum_shares=list(base.checksum_shares),
        global_integrity_check_share=base.global_integrity_check_share,
    )
    tampered_row.checksum_shares[0] = (tampered_row.checksum_shares[0] + 1) % FIELD_PRIME

    result = recover_mnemonic([tampered_row, shares[1]], 12, strict_validation=False)

    assert result.success is False
    assert result.errors["rowPathMismatch"] == [0]
    assert result.errors["row"] == [0]
    assert result.errors["globalPathMismatch"] is False
    assert result.errors["global"] is False


def test_recover_flags_global_path_mismatch():
    shares = split_mnemonic(VALID_MNEMONIC, 2, 3)
    base = shares[0]
    tampered_global = Share(
        share_number=base.share_number,
        word_shares=list(base.word_shares),
        checksum_shares=list(base.checksum_shares),
        global_integrity_check_share=(base.global_integrity_check_share + 1) % FIELD_PRIME,
    )

    result = recover_mnemonic([tampered_global, shares[1]], 12, strict_validation=False)

    assert result.success is False
    assert result.errors["globalPathMismatch"] is True
    assert result.errors["global"] is True
    assert result.errors["rowPathMismatch"] == []
    assert result.errors["row"] == []
