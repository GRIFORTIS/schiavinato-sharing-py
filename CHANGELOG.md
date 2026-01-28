# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2025-12-12

### Changed - BREAKING
- **BIP39 indexing is now 1-based (1-2048) instead of 0-based (0-2047)**
  - "abandon" is now index 0001 (was 0000)
  - "zoo" is now index 2048 (was 2047)
  - This aligns with human-centric design: people naturally count from 1, not 0
  - All APIs, error messages, and test vectors updated
  
### Changed - Share Display Format
- Share values now use dual-reference format for clarity:
  - Value 0: displayed as "0000-0000"
  - Values 1-2048: displayed as "[bip39word]-[4-digit-index]" (e.g., "abandon-0001", "zoo-2048")
  - Values 2049-2052: displayed as "2049-2049", "2050-2050", etc. (GF(2053) overflow values)
  
### Technical Details
- **Internal computation unchanged**: GF(2053) arithmetic still operates on field elements 0-2052
- **Only user-facing changes**: BIP39 word-to-index and index-to-word conversions adjusted (+1/-1)
- **Conversion functions updated**:
  - `mnemonic_to_indices()`: Returns 1-based indices (was 0-based)
  - `indices_to_mnemonic()`: Accepts 1-based indices (was 0-based)
  - `parse_input()`: Handles 1-2048 range for numeric input
- **Test vectors regenerated**: All test data updated with new indices
- **Error messages updated**: Range validation now shows "1-2048" instead of "0-2047"

### Migration Guide
- **If you have existing shares**: They are now invalid. This is a breaking change - regenerate all shares with v0.5.0
- **If you use the library**: Update to v0.5.0 and regenerate shares
- **API changes**: 
  - Functions that return indices now return 1-2048 (was 0-2047)
  - Functions that accept indices now expect 1-2048 (was 0-2047)
  
### Why This Change?
Schiavinato Sharing prioritizes human-centricity over computational convenience. While 0-based indexing is efficient for computers, the difference is negligible (a single add/subtract operation). The usability benefit of 1-based indexing for humans performing manual calculations is significant. "Word 1" being "abandon" with index 0001 is intuitive; explaining that "Word 1" has index 0000 creates unnecessary cognitive load, especially in inheritance scenarios where non-technical users must execute the scheme years after creation.

## [0.4.0] - 2025-12-09

### Added
- Dual-path checksum validation (Path A sums vs Path B polynomials) during split and recovery
- Checksum polynomial helpers (`sum_polynomials`, row/global checksum polynomials)
- Security utilities for constant-time comparisons and best-effort wiping
- Configurable randomness source for deterministic/testing scenarios
- Mnemonic/seed helpers (`generate_valid_mnemonic`, `mnemonic_to_indices`, `indices_to_mnemonic`, `parse_input`)
- **GIC Binding**: Global Integrity Check is now bound to share number `x` (printed GIC = sum + x mod 2053)

### Changed
- Recovery reports now surface `rowPathMismatch` and `globalPathMismatch` for checksum path disagreements
- Public API exports extended to match JS v0.4.0 surface
- **Terminology standardization**: "Global Checksum" renamed to "Global Integrity Check (GIC)" across all code, tests, and documentation
- Property name: `global_checksum_verification_share` → `global_integrity_check_share` (breaking change)
- Function name: `compute_global_checksum()` → `compute_global_integrity_check()` (breaking change)

### Tests/Docs
- Added dual-path checksum mismatch tests and random-source coverage
- Updated README to reflect new helpers and version

## [0.3.0] - 2025-12-06

### Changed
- Checksum shares are now computed deterministically as the sum of word shares (mod 2053) rather than using independent random polynomials
- This change enables share integrity validation during the splitting process
- Recovery algorithm unchanged - all existing shares remain recoverable
- Maintains all LSSS security properties

### Benefits
- Users can verify share integrity during manual splitting
- Row checksum share = sum of 3 word shares in that row (mod 2053)
- Global checksum share = sum of all word shares (mod 2053)
- Catches arithmetic errors before share distribution
- Zero impact on recovery time or process

### Security Note
- No information leakage (checksums are deterministic functions of words)
- Threshold property preserved (still requires k shares for recovery)
- Entropy source unchanged (word polynomials remain random)

### Migration
- No API changes required
- Shares created with earlier versions remain recoverable by v0.3.0
- Shares created with v0.3.0 remain recoverable by earlier versions
- The only difference is checksum computation method during split

## [0.1.0] - 2025-11-23

### Added
- Initial release of Schiavinato Sharing Python library
- Core GF(2053) field arithmetic operations
- Polynomial creation and evaluation
- Lagrange interpolation for secret reconstruction
- BIP39 mnemonic splitting with configurable k-of-n threshold
- BIP39 mnemonic recovery with comprehensive validation
- Row and global checksum computation and verification
- Type hints for all public APIs
- Support for both 12-word and 24-word mnemonics
- Compatible with Python 3.9+

### Security
- Uses `mnemonic` library for BIP39 validation
- Cryptographically secure random number generation via `secrets` module
- Rejection sampling to avoid modulo bias in random number generation

### Documentation
- Comprehensive README with API reference
- Docstrings on all public functions
- Security considerations and best practices
- Examples for common use cases

---

## Links

- **Repository**: https://github.com/GRIFORTIS/schiavinato-sharing-py
- **JavaScript Library**: https://github.com/GRIFORTIS/schiavinato-sharing-js
- **Specification**: https://github.com/GRIFORTIS/schiavinato-sharing-spec
- **Organization**: https://github.com/GRIFORTIS

---

[Unreleased]: https://github.com/GRIFORTIS/schiavinato-sharing-py/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/GRIFORTIS/schiavinato-sharing-py/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/GRIFORTIS/schiavinato-sharing-py/compare/v0.1.0...v0.3.0
[0.1.0]: https://github.com/GRIFORTIS/schiavinato-sharing-py/releases/tag/v0.1.0
