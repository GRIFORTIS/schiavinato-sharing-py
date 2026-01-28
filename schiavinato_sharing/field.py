"""
Galois Field GF(2053) Arithmetic

This module implements the core field arithmetic operations for Schiavinato Sharing.
All operations are performed modulo the prime 2053.

The prime 2053 was chosen because:
- It's larger than 2048 (BIP39 wordlist size)
- It's small enough for mental arithmetic
- It allows for compact share representations
"""

from typing import List, Tuple
import functools

# The prime modulus for the Galois field GF(2053)
FIELD_PRIME = 2053


def mod(value: int) -> int:
    """
    Reduces an integer into GF(2053) by applying modulo with wraparound for negatives.
    
    Args:
        value: The integer value to reduce
    
    Returns:
        The value reduced into the range [0, 2052]
    
    Examples:
        >>> mod(2055)
        2
        >>> mod(-1)
        2052
        >>> mod(2053)
        0
    """
    result = value % FIELD_PRIME
    return result if result >= 0 else result + FIELD_PRIME


def mod_add(a: int, b: int) -> int:
    """
    Adds two field elements and returns the result modulo 2053.
    
    Args:
        a: First field element
        b: Second field element
    
    Returns:
        (a + b) mod 2053
    
    Examples:
        >>> mod_add(2000, 100)
        47
        >>> mod_add(1000, 500)
        1500
    """
    return mod(a + b)


def mod_sub(a: int, b: int) -> int:
    """
    Subtracts the second field element from the first inside GF(2053).
    
    Args:
        a: First field element (minuend)
        b: Second field element (subtrahend)
    
    Returns:
        (a - b) mod 2053
    
    Examples:
        >>> mod_sub(100, 200)
        1953
        >>> mod_sub(1500, 500)
        1000
    """
    return mod(a - b)


def mod_mul(a: int, b: int) -> int:
    """
    Multiplies two field elements and reduces the product into GF(2053).
    
    Args:
        a: First field element
        b: Second field element
    
    Returns:
        (a * b) mod 2053
    
    Examples:
        >>> mod_mul(100, 50)
        841
        >>> mod_mul(2, 1026)
        2052
    """
    return mod(a * b)


def mod_inv(value: int) -> int:
    """
    Computes the multiplicative inverse of a non-zero field element.
    Uses the Extended Euclidean Algorithm.
    
    Args:
        value: The field element to invert (must be non-zero)
    
    Returns:
        The multiplicative inverse: value * result ≡ 1 (mod 2053)
    
    Raises:
        ValueError: If value is 0 or not invertible
    
    Examples:
        >>> mod_inv(2)
        1027
        >>> mod_inv(1027)
        2
    """
    val = mod(value)
    
    if val == 0:
        raise ValueError('Attempted to invert zero in GF(2053).')
    
    t, new_t = 0, 1
    r, new_r = FIELD_PRIME, val
    
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    
    if r > 1:
        raise ValueError('Value is not invertible in GF(2053).')
    
    if t < 0:
        t += FIELD_PRIME
    
    return t


def mod_div(a: int, b: int) -> int:
    """
    Division in GF(2053): a / b = a * b^(-1).
    
    Args:
        a: Dividend
        b: Divisor (must be non-zero)
    
    Returns:
        (a / b) mod 2053
    """
    return mod_mul(a, mod_inv(b))


def mod_pow(a: int, n: int) -> int:
    """
    Exponentiation in GF(2053).
    
    Args:
        a: Base
        n: Exponent
    
    Returns:
        a^n mod 2053
    """
    return pow(a, n, FIELD_PRIME)


# For backward compatibility with validation code
class GF2053:
    """Legacy class-based interface for GF(2053) arithmetic."""
    
    PRIME = FIELD_PRIME
    
    add = staticmethod(mod_add)
    sub = staticmethod(mod_sub)
    mul = staticmethod(mod_mul)
    inv = staticmethod(mod_inv)
    div = staticmethod(mod_div)
    pow = staticmethod(mod_pow)

