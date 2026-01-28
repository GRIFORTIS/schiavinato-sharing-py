"""
Polynomial Operations in GF(2053)

This module implements polynomial creation and evaluation for Shamir's Secret Sharing.
"""

import secrets
from typing import Callable, List, Optional
from .field import mod, mod_add, mod_mul, FIELD_PRIME

# Optional injectable randomness source for testing/parity with JS
_random_source: Optional[Callable[[int], bytes]] = None


def configure_random_source(source: Callable[[int], bytes]) -> None:
    """
    Configure a custom randomness provider.

    Args:
        source: Callable that accepts a byte count and returns bytes.
    """
    if source is None or not callable(source):
        raise ValueError("random source must be callable")
    # Basic contract check
    test = source(2)
    if not isinstance(test, (bytes, bytearray)) or len(test) != 2:
        raise ValueError("random source must return exactly the requested bytes")
    global _random_source
    _random_source = source


def get_random_field_element() -> int:
    """
    Generate a cryptographically secure random element in GF(2053).
    
    Returns:
        Random integer in [0, 2052]
    """
    # Generate random bytes and reduce to field
    # Use rejection sampling to avoid modulo bias
    while True:
        # Generate 4 bytes (32 bits) which gives range [0, 4294967295]
        random_bytes = (
            _random_source(4) if _random_source else secrets.token_bytes(4)
        )
        value = int.from_bytes(random_bytes, byteorder='big')

        # Accept if value < 4292877712 (2091673 * 2053, largest multiple that fits in 32 bits)
        # This ensures perfect uniform distribution with zero modulo bias
        # Rejection rate: 2089584 / 4294967296 ≈ 0.049%
        if value < 4292877712:
            return value % FIELD_PRIME


def random_polynomial(secret: int, degree: int) -> List[int]:
    """
    Builds a random polynomial of the requested degree whose constant term is the secret.
    
    For a (k,n) threshold scheme, we need a polynomial of degree k-1:
    f(x) = a₀ + a₁x + a₂x² + ... + aₖ₋₁xᵏ⁻¹
    
    where a₀ = secret and a₁...aₖ₋₁ are random coefficients.
    
    Args:
        secret: The secret value to share (becomes the constant term)
        degree: The degree of the polynomial (k-1 for k-threshold scheme)
    
    Returns:
        Array of coefficients [a₀, a₁, a₂, ..., aₖ₋₁]
    
    Examples:
        >>> # For a 2-of-n scheme (degree 1):
        >>> coeffs = random_polynomial(1679, 1)
        >>> len(coeffs)
        2
        >>> coeffs[0]
        1679
        
        >>> # For a 3-of-n scheme (degree 2):
        >>> coeffs = random_polynomial(1679, 2)
        >>> len(coeffs)
        3
        >>> coeffs[0]
        1679
    """
    coefficients = [mod(secret)]
    
    for _ in range(degree):
        coefficients.append(get_random_field_element())
    
    return coefficients


def evaluate_polynomial(coefficients: List[int], x: int) -> int:
    """
    Evaluates a polynomial at the provided x coordinate inside GF(2053).
    Uses Horner's method for efficient evaluation.
    
    For polynomial f(x) = a₀ + a₁x + a₂x² + ... + aₙxⁿ
    Horner's form: f(x) = a₀ + x(a₁ + x(a₂ + ... + x(aₙ)))
    
    Args:
        coefficients: Array of polynomial coefficients [a₀, a₁, ..., aₙ]
        x: The x coordinate at which to evaluate
    
    Returns:
        The polynomial value f(x) mod 2053
    
    Examples:
        >>> # Evaluate f(x) = 1679 + 456x at x=1
        >>> evaluate_polynomial([1679, 456], 1)
        82
        
        >>> # Evaluate f(x) = 1679 + 456x at x=2
        >>> evaluate_polynomial([1679, 456], 2)
        538
    """
    result = 0
    field_x = mod(x)
    
    # Horner's method: start from the highest degree coefficient
    for i in range(len(coefficients) - 1, -1, -1):
        result = mod_add(mod_mul(result, field_x), coefficients[i])
    
    return result

