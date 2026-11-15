from typing import Protocol

from tree_sitter import Tree

from codebase_assistant.domain.value_objects.source_format import SourceFormat


class Parser(Protocol):
    def parse(self, source_code: bytes, source_format: SourceFormat) -> Tree: ...
