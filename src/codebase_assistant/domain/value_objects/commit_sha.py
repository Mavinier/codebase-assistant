import re
from dataclasses import dataclass

_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$|^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CommitSHA:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("CommitSHA must be a string.")

        normalized = self.value.strip().lower()

        if not _SHA_PATTERN.match(normalized):
            raise ValueError(f"Invalid CommitSHA: '{self.value}")

        object.__setattr__(self, "value", normalized)

    def short(self, length: int = 7) -> str:
        return self.value[:length]

    def __str__(self) -> str:
        return self.value
