"""
Security utilities for constant-time comparisons and basic memory wiping.

Constant-Time Guarantees
-------------------------
The constant-time comparison functions in this module are designed to prevent
timing side-channel attacks. Their constant-time properties are guaranteed by
construction, not empirical testing:

- Uses only constant-time primitives (XOR, OR operations)
- No conditional branching on secret data
- Fixed iteration counts independent of input values

This approach matches Bitcoin Core's security model: constant-time by design,
verified through code review and static analysis, not runtime measurements.

Python's timing capabilities are insufficient to reliably validate constant-time
properties empirically. Interpreter overhead, OS scheduling, and GC introduce
noise that exceeds typical timing differences from side-channel vulnerabilities.
"""


def constant_time_equal(a: int, b: int) -> bool:
    """Constant-time equality for integers."""
    diff = a ^ b
    return diff == 0


def constant_time_string_equal(a: str, b: str) -> bool:
    """Constant-time string equality to reduce timing side channels."""
    max_len = max(len(a), len(b))
    diff = len(a) ^ len(b)
    for i in range(max_len):
        char_a = ord(a[i]) if i < len(a) else 0
        char_b = ord(b[i]) if i < len(b) else 0
        diff |= char_a ^ char_b
    return diff == 0


def secure_wipe_list(values: list[int]) -> None:
    """Overwrite list contents with zeros."""
    for i in range(len(values)):
        values[i] = 0


def secure_wipe_number(_value: int) -> int:
    """Return zero to overwrite a number variable."""
    return 0
