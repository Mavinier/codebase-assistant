from pathlib import Path

import pytest

from codebase_assistant.domain.value_objects.source_format import SourceFormat
from codebase_assistant.infrastructure.scanners.language_detector import (
    LanguageDetector,
)


@pytest.mark.parametrize(
    ("source_format", "expected_extension"),
    [
        (SourceFormat.TS, ".ts"),
        (SourceFormat.TSX, ".tsx"),
        (SourceFormat.JS, ".js"),
        (SourceFormat.JSX, ".jsx"),
        (".TS", ".ts"),
        (".TsX", ".tsx"),
        (".java.jsX", ".jsx"),
    ],
)
def test_should_detect_supported_languages(source_format, expected_extension) -> None:
    file_path = Path(f"src/test{source_format}")
    detector = LanguageDetector()
    result = detector.detect(file_path)

    assert result == expected_extension


def test_should_return_None_for_unsupported_languages() -> None:
    detector = LanguageDetector()
    result = detector.detect(Path("src/domain/makeLanguageDetector.Java"))

    assert result is None
