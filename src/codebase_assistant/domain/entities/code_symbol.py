from dataclasses import dataclass, field
from pathlib import Path

from codebase_assistant.domain.value_objects.symbol_id import SymbolId
from codebase_assistant.domain.value_objects.symbol_kind import SymbolKind
from codebase_assistant.domain.value_objects.symbol_location import SymbolLocation


@dataclass(frozen=True)
class CodeSymbol:
    id: SymbolId
    name: str = field(compare=False)
    kind: SymbolKind = field(compare=False)
    path: Path = field(compare=False)
    location: SymbolLocation = field(compare=False)
    parent_id: SymbolId | None = field(default=None, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.id, SymbolId):
            raise TypeError("'id' must be a SymbolId instance")

        if not isinstance(self.name, str):
            raise TypeError("'name' must be a string instance")

        if not self.name.strip():
            raise ValueError(
                "'name' must be a non-empty and not whitespace-only string"
            )

        if not isinstance(self.kind, SymbolKind):
            raise TypeError("'kind' must be a SymbolKind instance")

        if self.parent_id is not None and not isinstance(self.parent_id, SymbolId):
            raise TypeError("'parent_id' must be a SymbolId instance or None")

        if not isinstance(self.path, Path):
            raise TypeError("'path' must be a Path instance")

        if self.path.is_absolute() or ".." in self.path.parts:
            raise ValueError("'path' must be relative and not contain '..'")

        if not isinstance(self.location, SymbolLocation):
            raise TypeError("'location' must be a SymbolLocation instance")
