import tree_sitter_javascript as js
from tree_sitter import Language, Parser, Tree

from codebase_assistant.domain.interfaces.parser import Parser as ParserProtocol
from codebase_assistant.domain.value_objects.source_format import SourceFormat


class JavaScriptParser(ParserProtocol):
    def __init__(self):
        self.javascript_language = Language(js.language())

    def parse(self, source_code: bytes, source_format: SourceFormat) -> Tree:
        match source_format:
            case SourceFormat.JS | SourceFormat.JSX:
                language = self.javascript_language
            case _:
                raise ValueError(f"Unsupported format: '{source_format}'")

        parser = Parser(language)

        return parser.parse(source_code)
