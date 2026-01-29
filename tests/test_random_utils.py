import secrets

import pytest

from schiavinato_sharing import FIELD_PRIME, configure_random_source, get_random_field_element


def test_configure_random_source_rejects_bad_provider():
    with pytest.raises(ValueError):
        configure_random_source(lambda n: "not-bytes")  # type: ignore


def test_rejection_sampling_uses_retry_and_stays_in_field():
    calls = []

    def fake_random(byte_count: int) -> bytes:
        calls.append(byte_count)
        if len(calls) == 1:
            return (65000).to_bytes(2, "big")  # will be rejected (>=64512)
        return (1).to_bytes(2, "big")  # accepted

    configure_random_source(fake_random)
    value = get_random_field_element()

    # Ensure rejection happened and value is within the field
    assert len(calls) >= 2
    assert 0 <= value < FIELD_PRIME

    # Restore default secure source
    configure_random_source(secrets.token_bytes)
