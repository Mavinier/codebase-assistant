import pytest

from codebase_assistant.domain.value_objects.source_format import SourceFormat
from codebase_assistant.infrastructure.parsers.javascript_parser import JavaScriptParser


@pytest.fixture
def parser() -> JavaScriptParser:
    return JavaScriptParser()


def test_parse_javascript_file(parser: JavaScriptParser) -> None:
    source_code = b"""
    function greet(name) {
        return `Hello, ${name}`;
    };

    console.log(greet('Jhon'));
    """

    tree = parser.parse(source_code, SourceFormat.JS)

    assert tree.root_node.type == "program"
    assert not tree.root_node.has_error


def test_parse_jsx_file(parser: JavaScriptParser) -> None:
    source_code = b"""
    const App = () => {
        return <div>Hello World</div>;
    };
    """

    tree = parser.parse(source_code, SourceFormat.JSX)

    assert tree.root_node.type == "program"
    assert not tree.root_node.has_error


@pytest.mark.parametrize(
    "source_format",
    [
        SourceFormat.TS,
        SourceFormat.TSX,
    ],
)
def test_parse_unsupported_format(
    parser: JavaScriptParser, source_format: SourceFormat
) -> None:
    source_code = b"some unsupported content"

    with pytest.raises(ValueError, match="Unsupported format"):
        parser.parse(source_code, source_format)
