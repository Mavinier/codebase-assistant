import pytest
from tree_sitter import Tree

from codebase_assistant.domain.value_objects.source_format import SourceFormat
from codebase_assistant.infrastructure.parsers.parser_registry import ParserRegistry


class MockParser:
    def parse(self, source_code: bytes, source_format: SourceFormat) -> Tree:
        raise NotImplementedError


def test_get_parser_returns_registered_parser_for_source_format() -> None:
    ts_parser = MockParser()
    jsx_parser = MockParser()

    registry = ParserRegistry(
        {
            SourceFormat.TS: ts_parser,
            SourceFormat.JSX: jsx_parser,
        }
    )

    assert registry.get_parser(SourceFormat.TS) is ts_parser
    assert registry.get_parser(SourceFormat.JSX) is jsx_parser


def test_get_parser_raises_key_error_when_format_is_not_registered() -> None:
    tsx_parser = MockParser()

    registry = ParserRegistry({SourceFormat.TSX: tsx_parser})

    with pytest.raises(KeyError, match="Not available parser for"):
        registry.get_parser(SourceFormat.JSX)


def test_registry_makes_defensive_copy_of_input_mapping() -> None:
    ts_parser = MockParser()
    og_parsers = {SourceFormat.TS: ts_parser}
    registry = ParserRegistry(og_parsers)

    og_parsers.clear()
    og_parsers[SourceFormat.JS] = MockParser()

    assert registry.get_parser(SourceFormat.TS) is ts_parser

    with pytest.raises(KeyError, match="Not available parser for"):
        registry.get_parser(SourceFormat.JS)


def test_registry_internal_mapping_is_immutable() -> None:
    registry = ParserRegistry({SourceFormat.TS: MockParser()})

    with pytest.raises(TypeError):
        registry._parsers[SourceFormat.JS] = MockParser()
