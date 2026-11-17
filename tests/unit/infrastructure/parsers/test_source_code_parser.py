from pathlib import Path
from unittest.mock import Mock

import pytest
import tree_sitter_typescript as ts
from tree_sitter import Language, Parser

from codebase_assistant.domain.exceptions.source_format import (
    UnsupportedSourceFormatError,
)
from codebase_assistant.domain.value_objects.source_format import SourceFormat
from codebase_assistant.infrastructure.parsers.parser_registry import ParserRegistry
from codebase_assistant.infrastructure.parsers.source_code_parser import (
    SourceCodeParser,
)
from codebase_assistant.infrastructure.scanners.language_detector import (
    LanguageDetector,
)

# TODO: refactor test

def test_parse_returns_tree_for_supported_format() -> None:
    detector = LanguageDetector()
    path = Path("src/domain/makeLanguageDetector.tsx")
    source_code = b"""console.log('Hello!')"""

    language = Language(ts.language_tsx())
    tree_sitter_parser = Parser(language)
    expected_tree = tree_sitter_parser.parse(source_code)

    tsx_parser = Mock()
    tsx_parser.parse.return_value = expected_tree

    registry = ParserRegistry({SourceFormat.TSX: tsx_parser})

    source_code_parser = SourceCodeParser(detector, registry)

    result = source_code_parser.parse(path, source_code)

    assert result is expected_tree
    tsx_parser.parse.assert_called_once_with(source_code, SourceFormat.TSX)


def test_parse_raises_unsupported_source_format_exception() -> None:
    detector = Mock()
    detector.detect.return_value = None

    registry = ParserRegistry({})
    source_code_parser = SourceCodeParser(detector, registry)

    path = Path("src/domain/unknown.xyz")
    source_code = b"""unknown content"""

    with pytest.raises(UnsupportedSourceFormatError):
        source_code_parser.parse(path, source_code)

    detector.detect.assert_called_once_with(path)


def test_parse_propagates_key_error_when_parser_is_not_registered() -> None:
    detector = Mock()
    registry = Mock()

    detector.detect.return_value = SourceFormat.TSX
    registry.get_parser.side_effect = KeyError("Not available parser")

    source_code_parser = SourceCodeParser(detector, registry)

    path = Path("src/domain/test.tsx")
    source_code = b"""
    const App = () => {
        return <div>Hello World</div>;
    };
    """

    with pytest.raises(KeyError):
        source_code_parser.parse(path, source_code)

    registry.get_parser.assert_called_once_with(SourceFormat.TSX)
