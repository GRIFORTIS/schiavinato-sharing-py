"""
Integration tests using TEST_VECTORS.md

These tests verify the complete split and recover workflow using
the canonical test vectors from the specification.
"""

import pytest
from schiavinato_sharing import split_mnemonic, recover_mnemonic


class TestIntegration:
    """Integration tests with TEST_VECTORS.md data"""
    
    # Test mnemonic from TEST_VECTORS.md
    test_mnemonic = 'spin result brand ahead poet carpet unusual chronic denial festival toy autumn'
    
    # Expected shares from TEST_VECTORS.md (v0.5.0 - 1-based BIP39 indices)
    expected_shares = {
        1: {
            'share_number': 1,
            'word_shares': [83, 1573, 1343, 1045, 199, 850, 273, 680, 143, 812, 1966, 509],
            'checksum_shares': [946, 41, 1096, 1234],
            'global_integrity_check_share': 1264
        },
        2: {
            'share_number': 2,
            'word_shares': [539, 1675, 416, 2048, 1113, 1421, 692, 1036, 1871, 942, 35, 892],
            'checksum_shares': [577, 476, 1546, 1869],
            'global_integrity_check_share': 362
        },
        3: {
            'share_number': 3,
            'word_shares': [995, 1777, 1542, 998, 2027, 1992, 1111, 1392, 1546, 1072, 157, 1275],
            'checksum_shares': [208, 911, 1996, 451],
            'global_integrity_check_share': 1513
        }
    }
    
    def test_split_and_recover(self):
        """Test basic split and recover round-trip"""
        shares = split_mnemonic(self.test_mnemonic, 2, 3)
        
        assert len(shares) == 3
        
        # Use shares 1 and 2 to recover
        result = recover_mnemonic([shares[0], shares[1]], 12)
        
        assert result.success is True
        assert result.mnemonic == self.test_mnemonic
        assert len(result.errors['row']) == 0
        assert result.errors['global'] is False
        assert result.errors['bip39'] is False
    
    def test_all_share_combinations(self):
        """Test recovery works with any 2 of 3 shares"""
        shares = split_mnemonic(self.test_mnemonic, 2, 3)
        
        # Test all combinations
        combinations = [
            (0, 1),  # shares 1 and 2
            (0, 2),  # shares 1 and 3
            (1, 2)   # shares 2 and 3
        ]
        
        for i, j in combinations:
            result = recover_mnemonic([shares[i], shares[j]], 12)
            assert result.success is True
            assert result.mnemonic == self.test_mnemonic
    
    def test_overdetermined_recovery(self):
        """Test recovery with more than k shares"""
        shares = split_mnemonic(self.test_mnemonic, 2, 3)
        
        result = recover_mnemonic(shares, 12)
        
        assert result.success is True
        assert result.mnemonic == self.test_mnemonic
    
    def test_recovery_with_test_vectors(self):
        """Test recovery using exact test vector shares"""
        from schiavinato_sharing.types import Share
        
        # Create Share objects from test vectors
        share1 = Share(**self.expected_shares[1])
        share2 = Share(**self.expected_shares[2])
        
        result = recover_mnemonic([share1, share2], 12)
        
        assert result.success is True
        assert result.mnemonic == self.test_mnemonic
    
    def test_all_test_vector_combinations(self):
        """Test all combinations of test vector shares"""
        from schiavinato_sharing.types import Share
        
        shares = [
            Share(**self.expected_shares[1]),
            Share(**self.expected_shares[2]),
            Share(**self.expected_shares[3])
        ]
        
        combinations = [(0, 1), (0, 2), (1, 2)]
        
        for i, j in combinations:
            result = recover_mnemonic([shares[i], shares[j]], 12)
            assert result.success is True
            assert result.mnemonic == self.test_mnemonic
    
    def test_different_threshold_schemes(self):
        """Test various k-of-n schemes"""
        # 3-of-5 scheme
        shares = split_mnemonic(self.test_mnemonic, 3, 5)
        assert len(shares) == 5
        
        result = recover_mnemonic([shares[0], shares[2], shares[4]], 12)
        assert result.success is True
        assert result.mnemonic == self.test_mnemonic
        
        # 2-of-2 scheme
        shares = split_mnemonic(self.test_mnemonic, 2, 2)
        assert len(shares) == 2
        
        result = recover_mnemonic(shares, 12)
        assert result.success is True
        assert result.mnemonic == self.test_mnemonic
    
    def test_24_word_mnemonic(self):
        """Test with 24-word mnemonic"""
        mnemonic24 = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art'
        
        shares = split_mnemonic(mnemonic24, 2, 3)
        
        assert len(shares) == 3
        assert len(shares[0].word_shares) == 24
        assert len(shares[0].checksum_shares) == 8  # 24 / 3 = 8 rows
        
        result = recover_mnemonic([shares[0], shares[1]], 24)
        
        assert result.success is True
        assert result.mnemonic == mnemonic24
    
    def test_insufficient_shares(self):
        """Test that recovery fails with insufficient shares"""
        from schiavinato_sharing.types import Share
        
        share1 = Share(**self.expected_shares[1])
        
        result = recover_mnemonic([share1], 12)
        
        assert result.success is False
        assert 'At least two shares' in result.errors['generic']
    
    def test_duplicate_share_numbers(self):
        """Test that recovery fails with duplicate shares"""
        from schiavinato_sharing.types import Share
        
        share1 = Share(**self.expected_shares[1])
        
        result = recover_mnemonic([share1, share1], 12)
        
        assert result.success is False
        assert result.errors['generic'] is not None
        assert 'unique' in result.errors['generic'].lower()
