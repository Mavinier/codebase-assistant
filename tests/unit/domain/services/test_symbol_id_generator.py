from pathlib import Path

import pytest

from codebase_assistant.domain.services.symbol_id_generator import SymbolIdGenerator
from codebase_assistant.domain.value_objects.commit_sha import CommitSHA
from codebase_assistant.domain.value_objects.symbol_id import SymbolId
from codebase_assistant.domain.value_objects.symbol_kind import SymbolKind


def test_generate_valid_id() -> None:
    symbol_generator = SymbolIdGenerator()
    result = symbol_generator.generate(
        "id-1",
        CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
        Path("src/domain/service/typescript.ts"),
        SymbolKind.CLASS,
        "test-name",
        1,
        5,
    )
    assert isinstance(result, SymbolId)


def test_generate_deterministic() -> None:
    symbol_generator = SymbolIdGenerator()
    result = symbol_generator.generate(
        "id-1",
        CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
        Path("src/domain/service/typescript.ts"),
        SymbolKind.CLASS,
        "test-name",
        1,
        5,
    )
    regenerated = symbol_generator.generate(
        "id-1",
        CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
        Path("src/domain/service/typescript.ts"),
        SymbolKind.CLASS,
        "test-name",
        1,
        5,
    )
    assert result == regenerated


@pytest.mark.parametrize(
    "repository_id",
    [
        1234,
        "",
        " ",
    ],
)
def test_rejects_invalid_repository_id(repository_id: object) -> None:
    with pytest.raises(
        ValueError,
        match="'repository_id' must be a non-empty and not whitespace-only string",
    ):
        symbol_generator = SymbolIdGenerator()
        symbol_generator.generate(
            repository_id,
            CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
            Path("src/domain/service/typescript.ts"),
            SymbolKind.CLASS,
            "test-name",
            1,
            5,
        )


@pytest.mark.parametrize(
    "commit_sha",
    [
        1234,
        "",
        " ",
        "18482fb146ff52c24fc9cc19712efe9ba852e3427e59d36efff76f20f6d1d4c6",
    ],
)
def test_rejects_invalid_commit_sha(commit_sha: object) -> None:
    with pytest.raises(
        TypeError, match="'commit_sha' must be an instance of CommitSHA"
    ):
        symbol_generator = SymbolIdGenerator()
        symbol_generator.generate(
            "repository_id",
            commit_sha,
            Path("src/domain/service/typescript.ts"),
            SymbolKind.CLASS,
            "test-name",
            1,
            5,
        )


def test_rejects_invalid_file_path_instance() -> None:
    with pytest.raises(TypeError, match="'file_path' must be an instance of Path"):
        symbol_generator = SymbolIdGenerator()
        symbol_generator.generate(
            "repository_id",
            CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
            "src/domain/service/typescript.ts",
            SymbolKind.CLASS,
            "test-name",
            1,
            5,
        )


@pytest.mark.parametrize(
    "file_path",
    [
        Path("/src/domain/test.ts"),
        Path("src/domain/../test.ts"),
    ],
)
def test_rejects_invalid_file_path(file_path: object) -> None:
    with pytest.raises(
        ValueError, match="'file_path' must be relative and not contain '..'"
    ):
        symbol_generator = SymbolIdGenerator()
        symbol_generator.generate(
            "repository_id",
            CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
            file_path,
            SymbolKind.CLASS,
            "test-name",
            1,
            5,
        )


@pytest.mark.parametrize(
    "kind",
    ["simbol_kind", True, " "],
)
def test_rejects_invalid_kind(kind: object) -> None:
    with pytest.raises(TypeError, match="'kind' must be an instance of SymbolKind"):
        symbol_generator = SymbolIdGenerator()
        symbol_generator.generate(
            "repository_id",
            CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
            Path("src/domain/service/typescript.ts"),
            kind,
            "test-name",
            1,
            5,
        )


@pytest.mark.parametrize(
    "name",
    [
        1234,
        "",
        " ",
    ],
)
def test_rejects_invalid_name(name: object) -> None:
    with pytest.raises(
        ValueError, match="'name' must be a non-empty and not whitespace-only string"
    ):
        symbol_generator = SymbolIdGenerator()
        symbol_generator.generate(
            "repository_id",
            CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
            Path("src/domain/service/typescript.ts"),
            SymbolKind.CLASS,
            name,
            1,
            5,
        )


@pytest.mark.parametrize(
    ("start_byte", "end_byte"),
    [(True, 5), (1, True), ("1", 0), (1, 5.0)],
)
def test_rejects_invalid_byte_type(start_byte: object, end_byte: object) -> None:
    with pytest.raises(TypeError, match="'start_byte/end_byte' must be an integer"):
        symbol_generator = SymbolIdGenerator()
        symbol_generator.generate(
            "repository_id",
            CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
            Path("src/domain/service/typescript.ts"),
            SymbolKind.CLASS,
            "test-name",
            start_byte,
            end_byte,
        )


@pytest.mark.parametrize(
    ("start_byte", "end_byte"),
    [(-1, 5), (3, -3), (5, 3)],
)
def test_rejects_invalid_byte_value(start_byte: int, end_byte: int) -> None:
    with pytest.raises(ValueError):
        symbol_generator = SymbolIdGenerator()
        symbol_generator.generate(
            "repository_id",
            CommitSHA("cbda819156a1a5eedad38dc64871b8ca157df994"),
            Path("src/domain/service/typescript.ts"),
            SymbolKind.CLASS,
            "test-name",
            start_byte,
            end_byte,
        )
