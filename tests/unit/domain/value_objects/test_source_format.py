import pytest

from codebase_assistant.domain.value_objects.source_format import SourceFormat


@pytest.mark.parametrize(
    ("source_format", "expected_extension"),
    [
        (SourceFormat.TS, ".ts"),
        (SourceFormat.TSX, ".tsx"),
        (SourceFormat.JS, ".js"),
        (SourceFormat.JSX, ".jsx"),
    ],
)
def test_source_format_extension(
    source_format: SourceFormat,
    expected_extension: str,
) -> None:
    assert source_format.value == expected_extension
