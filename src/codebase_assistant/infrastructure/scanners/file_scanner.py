from pathlib import Path


class RepositoryFileScanner:
    def scan(self, repository_path: Path) -> list[Path]:
        if not repository_path.exists():
            raise FileNotFoundError(
                f"Repository path does not exist: {repository_path}"
            )

        if not repository_path.is_dir():
            raise NotADirectoryError(
                f"Repository path is not a directory: {repository_path}"
            )

        files = []

        for file_path in repository_path.rglob("*"):
            if not file_path.is_file():
                continue

            if any(part in self.IGNORED_DIRECTORIES for part in file_path.parts):
                continue

            if file_path.name in self.IGNORED_FILENAMES:
                continue

            if file_path.name.startswith(".env."):
                continue

            if file_path.suffix.lower() in self.IGNORED_EXTENSIONS:
                continue

            if file_path.suffix not in self.SUPPORTED_EXTENSIONS:
                continue

            files.append(file_path.relative_to(repository_path))

        return files

    SUPPORTED_EXTENSIONS = {
        # Source code
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        # Documentation
        ".md",
        ".mdx",
        # Configuration
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        # Database
        ".sql",
        ".prisma",
    }

    IGNORED_DIRECTORIES = {
        ".git",
        "node_modules",
        "dist",
        "build",
        "coverage",
        ".venv",
        "__pycache__",
    }

    IGNORED_FILENAMES = {
        ".env",
        ".netrc",
        ".npmrc",
        ".pypirc",
        "id_rsa",
        "id_ed25519",
        "credentials.json",
    }

    IGNORED_EXTENSIONS = {
        ".pem",
        ".key",
        ".p12",
        ".pfx",
    }
