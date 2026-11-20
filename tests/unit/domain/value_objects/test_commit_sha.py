from dataclasses import FrozenInstanceError

import pytest

from codebase_assistant.domain.value_objects.commit_sha import CommitSHA


@pytest.mark.parametrize(
    "value",
    [
        "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ],
)
def test_valid_sha_hashes(value: str) -> None:
    commit_sha = CommitSHA(value)
    assert commit_sha.value == value


@pytest.mark.parametrize(
    "value",
    [
        "   e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  ",
        "22A3C85609D4D626BC01CD87DF71D01F6BB9A62EFCE214D37B0D4FAF4F3EBB74",
        "  a94a8fe5ccb19ba61c4c0873d391e987982fbbd3 ",
        "A94A8FE5CCB19BA61C4C0873D391E987982FBBD3",
    ],
)
def test_normalized_sha_hash(value: str) -> None:
    commit_sha = CommitSHA(value)
    assert commit_sha.value == value.strip().lower()


@pytest.mark.parametrize(
    "value",
    [
        "e3b0c44298f c1c149afbf4c899 6fb92427 ae41e4649b934ca495991b7852b855",
        "22A3C856",
        "  a94a8fe5ccb19ba61c4c0 873d391e987982fbbd3 ",
        "A94A8FE5CCB19BÀ61Ç_C0873@391E987982FBBD3",
        "",
    ],
)
def test_reject_invalid_hash(value: object) -> None:
    with pytest.raises(ValueError, match="Invalid CommitSHA"):
        (CommitSHA(value))


@pytest.mark.parametrize(
    "value",
    [
        None,
        123,
    ],
)
def test_reject_not_str_hash(value: object) -> None:
    with pytest.raises(TypeError, match="CommitSHA must be a string"):
        (CommitSHA(value))


def test_commit_sha_is_immutable() -> None:
    VALID_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    symbol_id = CommitSHA(VALID_HASH)

    with pytest.raises(FrozenInstanceError):
        symbol_id.value = "a" * 64
