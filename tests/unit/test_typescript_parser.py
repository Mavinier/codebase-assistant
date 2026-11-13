import pytest

from codebase_assistant.infrastructure.parsers.typescript_parser import TypeScriptParser


@pytest.fixture
def parser() -> TypeScriptParser:
    return TypeScriptParser()


def test_parse_typescript_file(parser: TypeScriptParser) -> None:
    source_code = b"""
    interface User {
        name: string;
    }

    function greet(user: User): string {
        return `Hello, ${user.name}`;
    }
    """

    tree = parser.parse(source_code, ".ts")

    assert tree.root_node.type == "program"
    assert not tree.root_node.has_error


def test_parse_tsx_file(parser: TypeScriptParser) -> None:
    source_code = b"""
    const App = () => {
        return <div>Hello World</div>;
    };
    """

    tree = parser.parse(source_code, ".tsx")

    assert tree.root_node.type == "program"
    assert not tree.root_node.has_error


def test_parse_unsupported_extension(parser: TypeScriptParser) -> None:
    source_code = b"some unsupported content"

    with pytest.raises(ValueError, match="Unsupported extension"):
        parser.parse(source_code, ".html")
