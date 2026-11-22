import hashlib
import json
from pathlib import Path

from codebase_assistant.domain.value_objects.commit_sha import CommitSHA
from codebase_assistant.domain.value_objects.symbol_id import SymbolId
from codebase_assistant.domain.value_objects.symbol_kind import SymbolKind


class SymbolIdGenerator:
    def generate(
        self,
        repository_id: str,
        commit_sha: CommitSHA,
        file_path: Path,
        kind: SymbolKind,
        name: str,
        start_byte: int,
        end_byte: int,
    ) -> SymbolId:
        if not isinstance(repository_id, str):
            raise TypeError("'repository_id' must be a string instance")

        if not repository_id.strip():
            raise ValueError(
                "'repository_id' must be a non-empty and not whitespace-only string"
            )

        if not isinstance(commit_sha, CommitSHA):
            raise TypeError("'commit_sha' must be a CommitSHA instance")

        if not isinstance(file_path, Path):
            raise TypeError("'file_path' must be a Path instance")

        if file_path.is_absolute() or ".." in file_path.parts:
            raise ValueError("'file_path' must be relative and not contain '..'")

        if not isinstance(kind, SymbolKind):
            raise TypeError("'kind' must be a SymbolKind instance")

        if not isinstance(name, str):
            raise TypeError("'name' must be a string instance")

        if not name.strip():
            raise ValueError(
                "'name' must be a non-empty and not whitespace-only string"
            )

        if not all(
            isinstance(x, int) and not isinstance(x, bool)
            for x in (start_byte, end_byte)
        ):
            raise TypeError("'start_byte/end_byte' must be an integer")

        if start_byte < 0 or end_byte < 0:
            raise ValueError("'start_byte/end_byte' must not be negative")

        if start_byte > end_byte:
            raise ValueError("'start_byte' must not be greater than 'end_byte'")

        symbol_id_generator_dict = {
            "repository_id": repository_id,
            "commit_sha": commit_sha.value,
            "file_path": file_path.as_posix(),
            "kind": kind,
            "name": name,
            "start_byte": start_byte,
            "end_byte": end_byte,
        }

        serialized_json = json.dumps(
            symbol_id_generator_dict,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

        return SymbolId(hashlib.sha256(serialized_json.encode("utf-8")).hexdigest())
