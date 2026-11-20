import pytest

from codebase_assistant.domain.value_objects.symbol_kind import SymbolKind


@pytest.mark.parametrize(
    ("symbol_kind", "value"),
    [
        (SymbolKind.CLASS, "class"),
        (SymbolKind.FUNCTION, "function"),
        (SymbolKind.METHOD, "method"),
        (SymbolKind.INTERFACE, "interface"),
        (SymbolKind.VARIABLE, "variable"),
        (SymbolKind.PROPERTY, "property"),
        (SymbolKind.ENUM, "enum"),
    ],
)
def test_symbol_kind(symbol_kind: SymbolKind, value: str) -> None:
    assert symbol_kind.value == value


def test_symbol_kind_string_representation() -> None:
    string = f"{SymbolKind.CLASS}"
    assert isinstance(string, str)
    assert string == "class"


def test_rejects_invalid_symbol_kind() -> None:
    with pytest.raises(ValueError):
        (SymbolKind("override"))
