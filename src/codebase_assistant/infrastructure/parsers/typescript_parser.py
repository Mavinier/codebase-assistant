import tree_sitter_typescript as ts
from tree_sitter import Language, Parser, Tree

from codebase_assistant.domain.interfaces.parser import Parser as ParserProtocol
from codebase_assistant.domain.value_objects.source_format import SourceFormat


class TypeScriptParser(ParserProtocol):
    def __init__(self):
        self.typescript_language = Language(ts.language_typescript())
        self.tsx_language = Language(ts.language_tsx())

    def parse(self, source_code: bytes, source_format: SourceFormat) -> Tree:
        if source_format == SourceFormat.TS:
            language = self.typescript_language
        elif source_format == SourceFormat.TSX:
            language = self.tsx_language
        else:
            raise ValueError(f"Unsupported format: '{source_format}'")

        parser = Parser(language)

        return parser.parse(source_code)
