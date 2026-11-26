from pathlib import Path

from tree_sitter import Node, Tree

from codebase_assistant.domain.entities.code_symbol import CodeSymbol
from codebase_assistant.domain.services.symbol_id_generator import SymbolIdGenerator
from codebase_assistant.domain.value_objects.commit_sha import CommitSHA
from codebase_assistant.domain.value_objects.symbol_id import SymbolId
from codebase_assistant.domain.value_objects.symbol_kind import SymbolKind
from codebase_assistant.domain.value_objects.symbol_location import SymbolLocation


class SymbolExtractor:
    def __init__(self, symbol_id_generator: SymbolIdGenerator):
        self.symbol_id_generator = symbol_id_generator

    def extract(
        self, tree: Tree, repository_id: str, commit_sha: CommitSHA, file_path: Path
    ) -> list[CodeSymbol]:
        symbols: list[CodeSymbol] = []

        self._visit(
            node=tree.root_node,
            repository_id=repository_id,
            commit_sha=commit_sha,
            file_path=file_path,
            parent_id=None,
            symbols=symbols,
        )

        return symbols

    def _visit(
        self,
        node: Node,
        repository_id: str,
        commit_sha: CommitSHA,
        file_path: Path,
        parent_id: SymbolId | None,
        symbols: list[CodeSymbol],
    ) -> None:
        current_parent_id = parent_id

        if node.type == "function_declaration":
            symbol = self._build_symbol(
                node=node,
                repository_id=repository_id,
                commit_sha=commit_sha,
                file_path=file_path,
                parent_id=parent_id,
                kind=SymbolKind.FUNCTION,
            )
            if symbol is not None:
                symbols.append(symbol)
                current_parent_id = symbol.id

        elif node.type == "class_declaration":
            symbol = self._build_symbol(
                node=node,
                repository_id=repository_id,
                commit_sha=commit_sha,
                file_path=file_path,
                parent_id=parent_id,
                kind=SymbolKind.CLASS,
            )
            if symbol is not None:
                symbols.append(symbol)
                current_parent_id = symbol.id

        elif node.type == "method_definition":
            symbol = self._build_symbol(
                node=node,
                repository_id=repository_id,
                commit_sha=commit_sha,
                file_path=file_path,
                parent_id=parent_id,
                kind=SymbolKind.METHOD,
            )
            if symbol is not None:
                symbols.append(symbol)
                current_parent_id = symbol.id

        for child in node.named_children:
            self._visit(
                node=child,
                repository_id=repository_id,
                commit_sha=commit_sha,
                file_path=file_path,
                parent_id=current_parent_id,
                symbols=symbols,
            )

    def _build_symbol(
        self,
        node: Node,
        repository_id: str,
        commit_sha: CommitSHA,
        file_path: Path,
        parent_id: SymbolId | None,
        kind: SymbolKind,
    ) -> CodeSymbol | None:
        name_node = node.child_by_field_name("name")

        if name_node is None or name_node.text is None:
            return None

        name = name_node.text.decode("utf-8")
        start_line, start_column = node.start_point
        end_line, end_column = node.end_point
        symbol_location = SymbolLocation(start_line, end_line, start_column, end_column)

        symbol_id = self.symbol_id_generator.generate(
            repository_id=repository_id,
            commit_sha=commit_sha,
            file_path=file_path,
            kind=kind,
            name=name,
            start_byte=node.start_byte,
            end_byte=node.end_byte,
        )

        return CodeSymbol(
            id=symbol_id,
            name=name,
            kind=kind,
            path=file_path,
            location=symbol_location,
            parent_id=parent_id,
        )
