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


def test_extract_tree_with_no_declarations(parser: TypeScriptParser) -> None:
    tree = parser.parse(b"", SourceFormat.TS)
    symbol_extractor = SymbolExtractor(SymbolIdGenerator())
    symbols = symbol_extractor.extract(
        tree,
        "repository_id",
        CommitSHA("da39a3ee5e6b4b0d3255bfef95601890afd80709"),
        Path("src/test/test.ts"),
    )

    assert len(symbols) == 0


def test_extract_tree_with_class_declaration(parser: TypeScriptParser) -> None:
    tree = parser.parse(
        b"""
        class User {
            name: string;
            age: number;
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

    assert len(symbols) == 1
    symbol = symbols[0]

    assert symbol.name == "User"
    assert symbol.kind == SymbolKind.CLASS
    assert symbol.path == Path("src/test/test.ts")
    assert symbol.parent_id is None

    assert symbol.location == SymbolLocation(1, 4, 8, 9)


def test_extract_tree_with_nested_method(parser: TypeScriptParser) -> None:
    tree = parser.parse(
        b"""
        class User {
            name: string = "";

            greet(name: string): string {
                this.name = name;
                return(`Hello ${this.name}`)
            }
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

    assert not tree.root_node.has_error

    class_node = tree.root_node.named_children[0]
    class_body_node = class_node.child_by_field_name("body")
    method_node = class_body_node.named_children[1]

    assert len(symbols) == 2
    symbol = symbols[1]

    assert method_node.parent.type == "class_body"

    assert symbol.name == "greet"
    assert symbol.kind == SymbolKind.METHOD
    assert symbol.parent_id == symbols[0].id
    assert symbol.location == SymbolLocation(4, 7, 12, 13)


def test_extract_tree_with_object_literal_method(parser: TypeScriptParser) -> None:
    tree = parser.parse(
        b"""const obj = { greet() {} }""",
        SourceFormat.TS,
    )
    symbol_extractor = SymbolExtractor(SymbolIdGenerator())
    symbols = symbol_extractor.extract(
        tree,
        "repository_id",
        CommitSHA("da39a3ee5e6b4b0d3255bfef95601890afd80709"),
        Path("src/test/test.ts"),
    )

    lexical_declaration = tree.root_node.named_children[0]
    declarator_node = lexical_declaration.named_children[0]
    obj_node = declarator_node.child_by_field_name("value")
    method_node = obj_node.named_children[0]
    symbol = symbols[0]

    assert not tree.root_node.has_error
    assert len(symbols) == 1

    assert method_node.parent.type == "object"
    assert symbol.name == "greet"
    assert symbol.kind == SymbolKind.METHOD
    assert symbol.parent_id is None


def test_extract_tree_with_interface(parser: TypeScriptParser) -> None:
    tree = parser.parse(
        b"""
        interface User {
            name: string;
            age: number;
        }""",
        SourceFormat.TS,
    )
    symbol_extractor = SymbolExtractor(SymbolIdGenerator())
    symbols = symbol_extractor.extract(
        tree,
        "repository_id",
        CommitSHA("da39a3ee5e6b4b0d3255bfef95601890afd80709"),
        Path("src/test/test.ts"),
    )

    assert len(symbols) == 1
    symbol = symbols[0]

    assert not tree.root_node.has_error
    assert symbol.name == "User"
    assert symbol.kind == SymbolKind.INTERFACE
    assert symbol.path == Path("src/test/test.ts")
    assert symbol.parent_id is None

    assert symbol.location == SymbolLocation(1, 4, 8, 9)
