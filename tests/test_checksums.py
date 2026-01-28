"""
Tests for deterministic checksum computation (v0.3.0)

These tests verify that checksum shares are computed as the sum
of word shares, enabling share integrity validation during splitting.
"""

import pytest
from schiavinato_sharing import split_mnemonic
from schiavinato_sharing.field import mod_add, FIELD_PRIME


class TestDeterministicChecksums:
    """Test v0.3.0 deterministic checksum computation"""
    
    test_mnemonic = 'spin result brand ahead poet carpet unusual chronic denial festival toy autumn'
    
    def test_row_checksum_is_sum_of_words(self):
        """Verify row checksum share equals sum of 3 word shares in that row"""
        shares = split_mnemonic(self.test_mnemonic, 2, 3)
        
        for share in shares:
            # For each row
            for row in range(len(share.checksum_shares)):
                base = row * 3
                expected_checksum = mod_add(
                    mod_add(share.word_shares[base], share.word_shares[base + 1]),
                    share.word_shares[base + 2]
                )
                actual_checksum = share.checksum_shares[row]
                
                assert actual_checksum == expected_checksum, \
                    f"Share {share.share_number}, Row {row}: checksum mismatch"
    
    def test_global_checksum_is_sum_of_all_words(self):
        """Verify Global Integrity Check (GIC) share equals (sum of all word shares + share number)"""
        shares = split_mnemonic(self.test_mnemonic, 2, 3)
        
        for share in shares:
            global_sum = sum(share.word_shares) % FIELD_PRIME
            expected_bound_gic = (global_sum + share.share_number) % FIELD_PRIME
            actual_gic = share.global_integrity_check_share
            
            assert actual_gic == expected_bound_gic, \
                f"Share {share.share_number}: GIC mismatch"
    
    def test_test_vector_checksums(self):
        """Verify checksums match TEST_VECTORS.md examples using exact test vectors"""
        from schiavinato_sharing.types import Share
        
        # Use the exact test vector shares (not randomly generated) - v0.5.0 with 1-based indices
        share1 = Share(
            share_number=1,
            word_shares=[83, 1573, 1343, 1045, 199, 850, 273, 680, 143, 812, 1966, 509],
            checksum_shares=[946, 41, 1096, 1234],
            global_integrity_check_share=1264
        )
        
        share2 = Share(
            share_number=2,
            word_shares=[539, 1675, 416, 2048, 1113, 1421, 692, 1036, 1871, 942, 35, 892],
            checksum_shares=[577, 476, 1546, 1869],
            global_integrity_check_share=362
        )
        
        share3 = Share(
            share_number=3,
            word_shares=[995, 1777, 1542, 998, 2027, 1992, 1111, 1392, 1546, 1072, 157, 1275],
            checksum_shares=[208, 911, 1996, 451],
            global_integrity_check_share=1513
        )
        
        # Verify each share's checksums are deterministic sums
        for share in [share1, share2, share3]:
            for row in range(len(share.checksum_shares)):
                base = row * 3
                expected = mod_add(
                    mod_add(share.word_shares[base], share.word_shares[base + 1]),
                    share.word_shares[base + 2]
                )
                assert share.checksum_shares[row] == expected
            
            expected_global = sum(share.word_shares) % FIELD_PRIME
            assert share.global_integrity_check_share == expected_global
    
    def test_manual_verification_example(self):
        """Verify the manual calculation example from TEST_VECTORS.md"""
        from schiavinato_sharing.types import Share
        
        # Use the exact Share 1 from TEST_VECTORS.md (v0.5.0 - 1-based indices)
        share1 = Share(
            share_number=1,
            word_shares=[83, 1573, 1343, 1045, 199, 850, 273, 680, 143, 812, 1966, 509],
            checksum_shares=[946, 41, 1096, 1234],
            global_integrity_check_share=1264
        )
        
        # Share 1, Row 1 from TEST_VECTORS.md:
        # word_shares: [83, 1573, 1343, ...]
        # 83 + 1573 + 1343 = 2999 mod 2053 = 946
        
        row1_sum = share1.word_shares[0] + share1.word_shares[1] + share1.word_shares[2]
        row1_checksum = row1_sum % FIELD_PRIME
        
        assert row1_checksum == 946
        assert share1.checksum_shares[0] == 946
    
    def test_24_word_checksums(self):
        """Verify deterministic checksums work for 24-word mnemonics"""
        mnemonic24 = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art'
        
        shares = split_mnemonic(mnemonic24, 2, 3)
        
        for share in shares:
            # 24 words = 8 rows
            assert len(share.checksum_shares) == 8
            
            # Verify each row
            for row in range(8):
                base = row * 3
                expected = mod_add(
                    mod_add(share.word_shares[base], share.word_shares[base + 1]),
                    share.word_shares[base + 2]
                )
                assert share.checksum_shares[row] == expected
            
            # Verify Global Integrity Check (GIC) is bound to share number
            global_sum = sum(share.word_shares) % FIELD_PRIME
            expected_bound_gic = (global_sum + share.share_number) % FIELD_PRIME
            assert share.global_integrity_check_share == expected_bound_gic
    
    def test_different_thresholds_maintain_determinism(self):
        """Verify deterministic checksums work with different k values"""
        for k in [2, 3, 4]:
            shares = split_mnemonic(self.test_mnemonic, k, k + 1)
            
            for share in shares:
                # Verify row checksums
                for row in range(len(share.checksum_shares)):
                    base = row * 3
                    expected = mod_add(
                        mod_add(share.word_shares[base], share.word_shares[base + 1]),
                        share.word_shares[base + 2]
                    )
                    assert share.checksum_shares[row] == expected
                
                # Verify Global Integrity Check (GIC) is bound to share number
                global_sum = sum(share.word_shares) % FIELD_PRIME
                expected_bound_gic = (global_sum + share.share_number) % FIELD_PRIME
                assert share.global_integrity_check_share == expected_bound_gic
