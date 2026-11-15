import subprocess
from pathlib import Path

import pytest

from codebase_assistant.infrastructure.git.repository_inspector import (
    GitRepositoryInspector,
)


def create_git_repository(path: Path) -> Path:
    path.mkdir(parents=True)

    subprocess.run(
        ["git", "init", "-b", "master", str(path)],
        check=True,
        capture_output=True,
    )

    subprocess.run(
        ["git", "-C", str(path), "config", "user.name", "Test User"],
        check=True,
    )

    subprocess.run(
        ["git", "-C", str(path), "config", "user.email", "test@example.com"],
        check=True,
    )

    (path / "README.md").write_text("# Test repository")

    subprocess.run(
        ["git", "-C", str(path), "add", "."],
        check=True,
    )

    subprocess.run(
        ["git", "-C", str(path), "commit", "-m", "Initial commit"],
        check=True,
        capture_output=True,
    )

    return path


def test_inspect_returns_repository_metadata(tmp_path: Path) -> None:
    repository_path = create_git_repository(tmp_path / "repository")

    inspector = GitRepositoryInspector()

    revision = inspector.inspect(repository_path)

    assert revision.root == repository_path.resolve()
    assert revision.branch == "master"
    assert len(revision.commit_sha) == 40
    assert revision.is_dirty is False


def test_inspect_detects_dirty_repository(tmp_path: Path) -> None:
    repository_path = create_git_repository(tmp_path / "repository")

    (repository_path / "README.md").write_text("# Modified repository")

    inspector = GitRepositoryInspector()

    revision = inspector.inspect(repository_path)

    assert revision.is_dirty is True


def test_inspect_raises_when_path_does_not_exist(tmp_path: Path) -> None:
    inspector = GitRepositoryInspector()

    with pytest.raises(FileNotFoundError):
        inspector.inspect(tmp_path / "nonexistent")
