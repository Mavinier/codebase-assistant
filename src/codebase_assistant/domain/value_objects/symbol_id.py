import re
from dataclasses import dataclass

_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True)
class SymbolId:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not _SHA256_PATTERN.fullmatch(self.value):
            raise ValueError(
                "The SHA-256 hash must be a string "
                "of 64 lowercase hexadecimal characters."
            )

    def __str__(self) -> str:
        return self.value
