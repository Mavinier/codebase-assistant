from dataclasses import FrozenInstanceError

import pytest

from codebase_assistant.domain.value_objects.symbol_id import SymbolId


def test_valid_sha256_hash() -> None:
    VALID_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    symbol_id = SymbolId(VALID_HASH)
    assert symbol_id.value == VALID_HASH


@pytest.mark.parametrize(
    "value",
    [
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855eee",
        "e3b0c44298fc1c149afbf4c8996fb92427ae",
        123,
        None,
    ],
)
def test_rejects_invalid_hash(value: object) -> None:
    with pytest.raises(ValueError, match="The SHA-256 hash must be a string"):
        (SymbolId(value))


def test_symbol_id_is_immutable() -> None:
    VALID_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    symbol_id = SymbolId(VALID_HASH)

    with pytest.raises(FrozenInstanceError):
        symbol_id.value = "a" * 64
