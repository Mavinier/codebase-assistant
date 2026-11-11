from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepositoryRevision:
    root: Path
    branch: str | None
    commit_sha: str
    is_dirty: bool
