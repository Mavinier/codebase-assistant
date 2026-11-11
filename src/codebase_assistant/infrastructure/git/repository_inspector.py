import subprocess
from pathlib import Path

from codebase_assistant.domain.value_objects.repository_revision import (
    RepositoryRevision,
)


class GitRepositoryInspector:
    def inspect(self, repository_path: Path) -> RepositoryRevision:
        root = repository_path.resolve()

        if not root.exists():
            raise FileNotFoundError(f"Repository path does not exist: {root}")

        if not root.is_dir():
            raise NotADirectoryError(f"Repository path is not a directory: {root}")

        commit_sha = self._run_git(root, "rev-parse", "HEAD")
        branch = self._run_git(root, "branch", "--show-current")
        status = self._run_git(root, "status", "--porcelain")
        is_dirty = bool(status)

        return RepositoryRevision(
            root=root,
            branch=branch or None,
            commit_sha=commit_sha,
            is_dirty=is_dirty,
        )

    def _run_git(self, repository_path: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repository_path), *args],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()
