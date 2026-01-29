import itertools

import pytest

from schiavinato_sharing import generate_valid_mnemonic, recover_mnemonic, split_mnemonic


class TestComprehensiveSchemes:
    """
    Exhaustive combinatorial testing for required schemes:
    12/24 words: 2-of-3, 2-of-4, 3-of-5

    This ensures complete combinatorial coverage (e.g., verifying that
    *any* 3 shares out of 5 can recover the secret).
    """

    @pytest.mark.parametrize("word_count", [12, 24])
    @pytest.mark.parametrize(
        "k, n", [(2, 3), (2, 4), (3, 5)]  # 3 combinations  # 6 combinations  # 10 combinations
    )
    def test_all_combinations(self, word_count, k, n):
        # Generate ONE random seed
        mnemonic = generate_valid_mnemonic(word_count)

        # Split ONCE
        shares = split_mnemonic(mnemonic, k, n)
        assert len(shares) == n

        # Test EVERY valid combination of k shares
        combinations = list(itertools.combinations(shares, k))

        # Verify we are testing the correct number of combinations
        expected_combinations = {(2, 3): 3, (2, 4): 6, (3, 5): 10}[(k, n)]
        assert len(combinations) == expected_combinations

        for subset in combinations:
            result = recover_mnemonic(list(subset), word_count)

            # Full validation
            assert (
                result.success is True
            ), f"Failed recovery for k={k}, n={n} with subset {[s.share_number for s in subset]}"
            assert result.mnemonic == mnemonic
            assert result.errors["global"] is False
            assert len(result.errors["row"]) == 0
