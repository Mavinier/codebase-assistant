from pathlib import Path

import pytest

from codebase_assistant.domain.services.symbol_id_generator import SymbolIdGenerator
from codebase_assistant.domain.value_objects.commit_sha import CommitSHA
from codebase_assistant.domain.value_objects.source_format import SourceFormat
from codebase_assistant.domain.value_objects.symbol_kind import SymbolKind
from codebase_assistant.domain.value_objects.symbol_location import SymbolLocation
from codebase_assistant.infrastructure.parsers.symbol_extractor import SymbolExtractor
from codebase_assistant.infrastructure.parsers.typescript_parser import TypeScriptParser


@pytest.fixture
def parser() -> TypeScriptParser:
    return TypeScriptParser()


def test_extract_tree_declaration(parser: TypeScriptParser) -> None:
    tree = parser.parse(b"function greet() {}", SourceFormat.TS)
    symbol_extractor = SymbolExtractor(SymbolIdGenerator())
    symbols = symbol_extractor.extract(
        tree,
        "repository_id",
        CommitSHA("da39a3ee5e6b4b0d3255bfef95601890afd80709"),
        Path("src/test/test.ts"),
    )

    assert len(symbols) == 1
    symbol = symbols[0]

    assert symbol.name == "greet"
    assert symbol.kind == SymbolKind.FUNCTION
    assert symbol.path == Path("src/test/test.ts")
    assert symbol.parent_id is None

    assert symbol.location == SymbolLocation(0, 0, 0, 19)


def test_extract_tree_with_multiple_declarations(parser: TypeScriptParser) -> None:
    tree = parser.parse(
        b"""
        function greet() {}
        function name() {}
        function age() {}
    """,
        SourceFormat.TS,
    )
    symbol_extractor = SymbolExtractor(SymbolIdGenerator())
    symbols = symbol_extractor.extract(
        tree,
        "repository_id",
        CommitSHA("da39a3ee5e6b4b0d3255bfef95601890afd80709"),
        Path("src/test/test.ts"),
    )

    assert len(symbols) == 3

    assert [symbol.name for symbol in symbols] == ["greet", "name", "age"]

    assert [symbol.location for symbol in symbols] == [
        SymbolLocation(1, 1, 8, 27),
        SymbolLocation(2, 2, 8, 26),
        SymbolLocation(3, 3, 8, 25),
    ]


def test_extract_tree_with_nested_declaration(parser: TypeScriptParser) -> None:
    tree = parser.parse(
        b"""
        function outer() {
            function inner() {}
        }
    """,
        SourceFormat.TS,
    )
    symbol_extractor = SymbolExtractor(SymbolIdGenerator())
    symbols = symbol_extractor.extract(
        tree,
        "repository_id",
        CommitSHA("da39a3ee5e6b4b0d3255bfef95601890afd80709"),
        Path("src/test/test.ts"),
    )

    assert len(symbols) == 2
    assert symbols[1].parent_id == symbols[0].id
    assert [symbol.name for symbol in symbols] == ["outer", "inner"]
