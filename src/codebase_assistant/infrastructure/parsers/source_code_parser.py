from pathlib import Path

from tree_sitter import Tree

from codebase_assistant.domain.exceptions.source_format import (
    UnsupportedSourceFormatError,
)
from codebase_assistant.infrastructure.parsers.parser_registry import ParserRegistry
from codebase_assistant.infrastructure.scanners.language_detector import (
    LanguageDetector,
)


class SourceCodeParser:
    def __init__(
        self, language_detector: LanguageDetector, parser_registry: ParserRegistry
    ):
        self.language_detector = language_detector
        self.parser_registry = parser_registry

    def parse(self, file_path: Path, source_code: bytes) -> Tree:
        source_format = self.language_detector.detect(file_path)

        if source_format is None:
            raise UnsupportedSourceFormatError(
                f"Unsupported source format: {file_path.suffix}"
            )

        parser = self.parser_registry.get_parser(source_format)
        return parser.parse(source_code, source_format)
