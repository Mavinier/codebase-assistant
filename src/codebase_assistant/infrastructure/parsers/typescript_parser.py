import tree_sitter_typescript as ts
from tree_sitter import Language, Parser, Tree


class TypeScriptParser:
    def __init__(self):
        self.typescript_language = Language(ts.language_typescript())
        self.tsx_language = Language(ts.language_tsx())

    def parse(self, source_code: bytes, file_extension: str) -> Tree:
        if file_extension == ".ts":
            language = self.typescript_language
        elif file_extension == ".tsx":
            language = self.tsx_language
        else:
            raise ValueError(f"Unsupported extension: '{file_extension}'")

        parser = Parser(language)

        return parser.parse(source_code)
