from schiavinato_sharing import split_mnemonic, WORDS_PER_ROW, mod_add


def test_split_checksums_self_consistent():
    mnemonic = (
        "spin result brand ahead poet carpet unusual chronic denial festival toy autumn"
    )
    shares = split_mnemonic(mnemonic, 2, 3)

    for share in shares:
        # Row checksums must equal sum of 3 word shares per row
        row_count = len(share.word_shares) // WORDS_PER_ROW
        for row in range(row_count):
            base = row * WORDS_PER_ROW
            expected = mod_add(
                mod_add(share.word_shares[base], share.word_shares[base + 1]),
                share.word_shares[base + 2],
            )
            assert share.checksum_shares[row] == expected

        # Global Integrity Check (GIC) must equal (sum of all word shares + share number) mod 2053
        global_sum = 0
        for val in share.word_shares:
            global_sum = mod_add(global_sum, val)
        expected_bound_gic = mod_add(global_sum, share.share_number)
        assert share.global_integrity_check_share == expected_bound_gic
