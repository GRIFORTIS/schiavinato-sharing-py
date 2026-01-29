from schiavinato_sharing.checksums import (
    compute_global_check_polynomial,
    compute_row_check_polynomials,
)
from schiavinato_sharing.field import mod_add
from schiavinato_sharing.polynomial import evaluate_polynomial


class TestVectorsExactReproduction:
    """
    Exact reproduction of TEST_VECTORS.md logic.

    This test validates that our implementation produces shares that match
    TEST_VECTORS.md exactly when using the same coefficients.

    IMPORTANT: This test does NOT modify production code. It manually constructs
    polynomials using the known coefficients from TEST_VECTORS.md and validates
    the mathematical operations (polynomial evaluation, checksum computation).
    """

    # From TEST_VECTORS.md Section 3.1
    TEST_MNEMONIC = "spin result brand ahead poet carpet unusual chronic denial festival toy autumn"
    WORD_INDICES = [1680, 1471, 217, 42, 1338, 279, 1907, 324, 468, 682, 1844, 126]

    # From TEST_VECTORS.md Section 3.4 (Exact random coefficients)
    COEFFICIENTS = [1, 2052, 1126, 2012, 710, 571, 146, 1728, 2000, 130, 122, 383]

    # Expected shares from TEST_VECTORS.md Section 5
    EXPECTED_SHARES = {
        1: {
            "word_shares": [1681, 1470, 1343, 1, 2048, 850, 0, 2052, 415, 812, 1966, 509],
            "checksum_shares": [388, 846, 414, 1234],
            "gic_share": 830,
        },
        2: {
            "word_shares": [1682, 1469, 416, 2013, 705, 1421, 146, 1727, 362, 942, 35, 892],
            "checksum_shares": [1514, 33, 182, 1869],
            "gic_share": 1547,
        },
        3: {
            "word_shares": [1683, 1468, 1542, 1972, 1415, 1992, 292, 1402, 309, 1072, 157, 1275],
            "checksum_shares": [587, 1273, 2003, 451],
            "gic_share": 211,
        },
    }

    def test_manual_polynomial_construction(self):
        """
        Manually construct polynomials using exact coefficients from spec
        and verify they produce the exact expected shares.
        """
        # Construct word polynomials f(x) = a0 + a1*x manually
        # Each polynomial is [a0, a1] (constant term, x^1 term)
        word_polynomials = [
            [secret, coeff]
            for secret, coeff in zip(self.WORD_INDICES, self.COEFFICIENTS, strict=True)
        ]

        # Compute derived checksum polynomials (deterministic)
        row_polys = compute_row_check_polynomials(word_polynomials)
        gic_poly = compute_global_check_polynomial(word_polynomials)

        for x in [1, 2, 3]:
            expected = self.EXPECTED_SHARES[x]

            # 1. Verify Word Shares
            generated_words = [evaluate_polynomial(p, x) for p in word_polynomials]
            assert generated_words == expected["word_shares"], f"Word shares mismatch for share {x}"

            # 2. Verify Row Checksum Shares
            generated_rows = [evaluate_polynomial(p, x) for p in row_polys]
            assert (
                generated_rows == expected["checksum_shares"]
            ), f"Checksum shares mismatch for share {x}"

            # 3. Verify Global Integrity Check Share
            # Note: GIC share includes +x binding per spec
            gic_base = evaluate_polynomial(gic_poly, x)
            gic_share = mod_add(gic_base, x)
            assert gic_share == expected["gic_share"], f"GIC mismatch for share {x}"
