from pathlib import Path

import pytest

from codebase_assistant.infrastructure.scanners.file_scanner import (
    RepositoryFileScanner,
)


def test_scan_returns_supported_files(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "App.tsx").write_text("export const App = () => null")
    (tmp_path / "README.md").write_text("# Project")
    (tmp_path / "image.png").write_bytes(b"fake-image")

    scanner = RepositoryFileScanner()

    result = scanner.scan(tmp_path)

    assert Path("src/App.tsx") in result
    assert Path("README.md") in result
    assert Path("image.png") not in result


def test_scan_ignores_excluded_directories(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "node_modules" / "package").mkdir(parents=True)

    (tmp_path / "src" / "App.tsx").write_text("export const App = () => null")
    (tmp_path / "node_modules" / "package" / "index.js").write_text(
        "module.exports = {}"
    )

    scanner = RepositoryFileScanner()

    result = scanner.scan(tmp_path)

    assert Path("src/App.tsx") in result
    assert Path("node_modules/package/index.js") not in result


def test_scan_ignores_environment_files(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()

    (tmp_path / "src" / "App.tsx").write_text("export const App = () => null")
    (tmp_path / ".env").write_text("API_KEY=secret")

    scanner = RepositoryFileScanner()

    result = scanner.scan(tmp_path)

    assert Path("src/App.tsx") in result
    assert Path(".env") not in result


def test_scan_returns_configuration_and_database_files(
    tmp_path: Path,
) -> None:
    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "tsconfig.json").write_text("{}")
    (tmp_path / "schema.prisma").write_text("")
    (tmp_path / "migration.sql").write_text("SELECT 1")

    scanner = RepositoryFileScanner()

    result = scanner.scan(tmp_path)

    assert Path("package.json") in result
    assert Path("tsconfig.json") in result
    assert Path("schema.prisma") in result
    assert Path("migration.sql") in result


def test_scan_ignores_sensitive_files(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()

    (tmp_path / "src" / "App.tsx").write_text("export const App = () => null")
    (tmp_path / ".env").write_text("API_KEY=secret")
    (tmp_path / ".env.production").write_text("API_KEY=secret")
    (tmp_path / "private.pem").write_text("private key")
    (tmp_path / "id_rsa").write_text("private key")
    (tmp_path / ".npmrc").write_text("//registry.npmjs.org/:_authToken=secret")
    (tmp_path / "credentials.json").write_text('{"token": "secret"}')

    scanner = RepositoryFileScanner()

    result = scanner.scan(tmp_path)

    assert Path("src/App.tsx") in result
    assert Path(".env") not in result
    assert Path(".env.production") not in result
    assert Path("private.pem") not in result
    assert Path("id_rsa") not in result
    assert Path(".npmrc") not in result
    assert Path("credentials.json") not in result


def test_scan_raises_error_when_repository_does_not_exist(
    tmp_path: Path,
) -> None:
    repository_path = tmp_path / "nonexistent"

    scanner = RepositoryFileScanner()

    with pytest.raises(FileNotFoundError):
        scanner.scan(repository_path)


def test_scan_raises_error_when_path_is_a_file(
    tmp_path: Path,
) -> None:
    repository_path = tmp_path / "README.md"
    repository_path.write_text("# Project")

    scanner = RepositoryFileScanner()

    with pytest.raises(NotADirectoryError):
        scanner.scan(repository_path)
