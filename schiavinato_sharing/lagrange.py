"""
Lagrange Interpolation in GF(2053)

This module implements Lagrange interpolation for secret reconstruction
in Shamir's Secret Sharing over the finite field GF(2053).
"""

from typing import List, Tuple
from .field import mod, mod_add, mod_sub, mod_mul, mod_inv, FIELD_PRIME


def lagrange_interpolate_at_zero(points: List[Tuple[int, int]]) -> int:
    """
    Applies Lagrange interpolation at x=0 to recover the secret from share points.
    
    For points (x₁,y₁), (x₂,y₂), ..., (xₖ,yₖ), computes:
    
    f(0) = Σⱼ yⱼ · Lⱼ(0)
    
    where Lⱼ(0) is the Lagrange basis polynomial evaluated at x=0:
    
    Lⱼ(0) = ∏ₘ≠ⱼ (0 - xₘ) / (xⱼ - xₘ) = ∏ₘ≠ⱼ (-xₘ) / (xⱼ - xₘ)
    
    Args:
        points: List of (x,y) coordinate pairs
    
    Returns:
        The secret value f(0)
    
    Raises:
        ValueError: If points list is empty
    
    Examples:
        >>> # Recover secret from 2 shares
        >>> lagrange_interpolate_at_zero([(1, 82), (2, 538)])
        1679
    """
    if not points or len(points) == 0:
        raise ValueError('Interpolation requires at least one point.')
    
    sum_val = 0
    
    for j in range(len(points)):
        numerator = 1
        denominator = 1
        
        xj = mod(points[j][0])
        yj = mod(points[j][1])
        
        # Compute the Lagrange basis polynomial Lⱼ(0)
        for m in range(len(points)):
            if m == j:
                continue
            
            xm = mod(points[m][0])
            
            # Numerator: ∏ₘ≠ⱼ (0 - xₘ) = ∏ₘ≠ⱼ (-xₘ)
            numerator = mod_mul(numerator, mod(FIELD_PRIME - xm))
            
            # Denominator: ∏ₘ≠ⱼ (xⱼ - xₘ)
            denominator = mod_mul(denominator, mod_sub(xj, xm))
        
        # Compute yⱼ · Lⱼ(0) = yⱼ · (numerator / denominator)
        term = mod_mul(yj, mod_mul(numerator, mod_inv(denominator)))
        sum_val = mod_add(sum_val, term)
    
    return sum_val


def compute_lagrange_multipliers(share_numbers: List[int]) -> List[int]:
    """
    Computes the Lagrange multipliers (λ) for the provided share numbers at X=0.
    
    These multipliers can be pre-computed and used for manual recovery:
    secret = λ₁·y₁ + λ₂·y₂ + ... + λₖ·yₖ (mod 2053)
    
    For share numbers x₁, x₂, ..., xₖ, the multiplier for share i is:
    
    λᵢ = ∏ⱼ≠ᵢ (0 - xⱼ) / (xᵢ - xⱼ) = ∏ⱼ≠ᵢ (-xⱼ) / (xᵢ - xⱼ)
    
    Args:
        share_numbers: List of share numbers (X coordinates)
    
    Returns:
        List of Lagrange multipliers in the same order as shareNumbers
    
    Raises:
        ValueError: If share numbers are invalid, duplicate, or contain zero
    
    Examples:
        >>> # Compute multipliers for shares {1, 2}
        >>> compute_lagrange_multipliers([1, 2])
        [2, 2052]
        
        >>> # Compute multipliers for shares {1, 3}
        >>> compute_lagrange_multipliers([1, 3])
        [1028, 1026]
    """
    if not share_numbers or len(share_numbers) < 2:
        raise ValueError('At least two share numbers are required to compute multipliers.')
    
    # Normalize to field
    normalized = [mod(x) for x in share_numbers]
    
    # Check for duplicates and zeros
    seen = set()
    for value in normalized:
        if value == 0:
            raise ValueError('Share numbers cannot be zero.')
        if value in seen:
            raise ValueError('Share numbers must be unique.')
        seen.add(value)
    
    multipliers = []
    
    for i in range(len(normalized)):
        numerator = 1
        denominator = 1
        
        xi = mod(normalized[i])
        
        for j in range(len(normalized)):
            if i == j:
                continue
            
            xj = mod(normalized[j])
            
            # Numerator: ∏ⱼ≠ᵢ (0 - xⱼ) = ∏ⱼ≠ᵢ (-xⱼ)
            numerator = mod_mul(numerator, mod(FIELD_PRIME - xj))
            
            # Denominator: ∏ⱼ≠ᵢ (xᵢ - xⱼ)
            denominator = mod_mul(denominator, mod_sub(xi, xj))
        
        multipliers.append(mod_mul(numerator, mod_inv(denominator)))
    
    return multipliers

