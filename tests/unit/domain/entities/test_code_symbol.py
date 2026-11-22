from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from codebase_assistant.domain.entities.code_symbol import CodeSymbol
from codebase_assistant.domain.value_objects.symbol_id import SymbolId
from codebase_assistant.domain.value_objects.symbol_kind import SymbolKind
from codebase_assistant.domain.value_objects.symbol_location import SymbolLocation


def test_valid_code_symbol() -> None:
    location = SymbolLocation(1, 1, 2, 5)
    code_symbol = CodeSymbol(
        SymbolId("18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"),
        "code_symbol_name",
        SymbolKind.CLASS,
        Path("src/domain/service/typescript.ts"),
        location,
        None,
    )
    assert isinstance(code_symbol, CodeSymbol)


def test_code_symbol_is_immutable() -> None:
    location = SymbolLocation(1, 1, 2, 5)
    code_symbol = CodeSymbol(
        SymbolId("18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"),
        "code_symbol_name",
        SymbolKind.CLASS,
        Path("src/domain/service/typescript.ts"),
        location,
        None,
    )
    with pytest.raises(FrozenInstanceError):
        code_symbol.name = "New_name"


def test_code_symbol_is_equal() -> None:
    location = SymbolLocation(1, 1, 2, 5)
    code_symbol_a = CodeSymbol(
        SymbolId("18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"),
        "code_symbol_name_A",
        SymbolKind.CLASS,
        Path("src/domain/service/typescript.ts"),
        location,
        None,
    )

    code_symbol_b = CodeSymbol(
        SymbolId("18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"),
        "code_symbol_name_B",
        SymbolKind.CLASS,
        Path("src/domain/service/typescript.ts"),
        location,
        None,
    )

    code_symbol_c = CodeSymbol(
        SymbolId("1d49808e6f250476f92dc903b128216ed106a77ae76ce8072f5c13a2caff8e81"),
        "code_symbol_name_B",
        SymbolKind.CLASS,
        Path("src/domain/service/typescript.ts"),
        location,
        None,
    )

    assert code_symbol_a != code_symbol_c
    assert code_symbol_b != code_symbol_c
    assert code_symbol_a == code_symbol_b


def test_parent_id_none_as_default() -> None:
    location = SymbolLocation(1, 1, 2, 5)
    code_symbol = CodeSymbol(
        SymbolId("18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"),
        "code_symbol_name",
        SymbolKind.CLASS,
        Path("src/domain/service/typescript.ts"),
        location,
    )
    assert isinstance(code_symbol, CodeSymbol)


@pytest.mark.parametrize(
    "id",
    [
        1234,
        "",
        " ",
    ],
)
def test_rejects_invalid_id(id: object) -> None:
    location = SymbolLocation(1, 1, 2, 5)

    with pytest.raises(
        TypeError,
        match="'id' must be a SymbolId instance",
    ):
        CodeSymbol(
            id,
            "code_symbol_name_B",
            SymbolKind.CLASS,
            Path("src/domain/service/typescript.ts"),
            location,
            None,
        )


@pytest.mark.parametrize(
    "name",
    [134, 1.23, None, True],
)
def test_rejects_invalid_name_instance(name: object) -> None:
    location = SymbolLocation(1, 1, 2, 5)

    with pytest.raises(
        TypeError,
        match="'name' must be a string instance",
    ):
        CodeSymbol(
            SymbolId(
                "18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"
            ),
            name,
            SymbolKind.CLASS,
            Path("src/domain/service/typescript.ts"),
            location,
            None,
        )


@pytest.mark.parametrize(
    "name",
    [
        "",
        " ",
    ],
)
def test_rejects_invalid_name_value(name: object) -> None:
    location = SymbolLocation(1, 1, 2, 5)

    with pytest.raises(
        ValueError,
        match="'name' must be a non-empty and not whitespace-only string",
    ):
        CodeSymbol(
            SymbolId(
                "18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"
            ),
            name,
            SymbolKind.CLASS,
            Path("src/domain/service/typescript.ts"),
            location,
            None,
        )


@pytest.mark.parametrize(
    "kind",
    [
        "kind_test",
        "",
        " ",
        1234,
    ],
)
def test_rejects_invalid_kind(kind: object) -> None:
    location = SymbolLocation(1, 1, 2, 5)

    with pytest.raises(
        TypeError,
        match="'kind' must be a SymbolKind instance",
    ):
        CodeSymbol(
            SymbolId(
                "18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"
            ),
            "code_symbol_name_B",
            kind,
            Path("src/domain/service/typescript.ts"),
            location,
            None,
        )


@pytest.mark.parametrize(
    "parent_id",
    [
        "kind_test",
        "",
        " ",
        1234,
    ],
)
def test_rejects_invalid_parent_id(parent_id: object) -> None:
    location = SymbolLocation(1, 1, 2, 5)

    with pytest.raises(
        TypeError,
        match="'parent_id' must be a SymbolId instance or None",
    ):
        CodeSymbol(
            SymbolId(
                "18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"
            ),
            "code_symbol_name_B",
            SymbolKind.CLASS,
            Path("src/domain/service/typescript.ts"),
            location,
            parent_id,
        )


def test_rejects_invalid_path_instance() -> None:
    location = SymbolLocation(1, 1, 2, 5)

    with pytest.raises(
        TypeError,
        match="'path' must be a Path instance",
    ):
        CodeSymbol(
            SymbolId(
                "18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"
            ),
            "code_symbol_name_B",
            SymbolKind.CLASS,
            "src/domain/service/typescript.ts",
            location,
            None,
        )


@pytest.mark.parametrize(
    "path",
    [
        Path("/src/domain/test.ts"),
        Path("src/domain/../test.ts"),
    ],
)
def test_rejects_invalid_path_value(path: object) -> None:
    location = SymbolLocation(1, 1, 2, 5)

    with pytest.raises(
        ValueError,
        match="'path' must be relative and not contain '..'",
    ):
        CodeSymbol(
            SymbolId(
                "18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"
            ),
            "code_symbol_name",
            SymbolKind.CLASS,
            path,
            location,
            None,
        )


@pytest.mark.parametrize(
    "location",
    [
        1234,
        "",
        " ",
    ],
)
def test_rejects_invalid_location(location: object) -> None:
    with pytest.raises(
        TypeError,
        match="'location' must be a SymbolLocation instance",
    ):
        CodeSymbol(
            SymbolId(
                "18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6"
            ),
            "code_symbol_name_B",
            SymbolKind.CLASS,
            Path("src/domain/service/typescript.ts"),
            location,
            None,
        )
