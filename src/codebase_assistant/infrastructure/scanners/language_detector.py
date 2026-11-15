from pathlib import Path

from codebase_assistant.domain.value_objects.source_format import SourceFormat


class LanguageDetector:
    def detect(self, file_path: Path) -> SourceFormat | None:
        extension = file_path.suffix.lower()

        try:
            return SourceFormat(extension)
        except ValueError:
            return None
