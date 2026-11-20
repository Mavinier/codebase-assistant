from dataclasses import FrozenInstanceError

import pytest

from codebase_assistant.domain.value_objects.symbol_location import SymbolLocation


@pytest.mark.parametrize(
    ("start_line", "end_line", "start_column", "end_column"),
    [(0, 0, 0, 0), (0, 1, 2, 5)],
)
def test_valid_locations(
    start_line: int, end_line: int, start_column: int, end_column: int
) -> None:
    location = SymbolLocation(start_line, end_line, start_column, end_column)

    assert location.start_line == start_line
    assert location.end_line == end_line
    assert location.start_column == start_column
    assert location.end_column == end_column


@pytest.mark.parametrize(
    ("start_line", "end_line", "start_column", "end_column"),
    [(-1, 0, 0, 0), (0, -1, 2, 5), (1, 1, 3, -1), (0, 1, -3, 4)],
)
def test_rejects_negative_values(
    start_line: int, end_line: int, start_column: int, end_column: int
) -> None:
    with pytest.raises(ValueError):
        SymbolLocation(start_line, end_line, start_column, end_column)


@pytest.mark.parametrize(
    ("start_line", "end_line", "start_column", "end_column"),
    [(True, 0, False, True), (1.0, 1, 2, 5), ("1", 1, 3, 5)],
)
def test_rejects_invalid_types(
    start_line: int, end_line: int, start_column: int, end_column: int
) -> None:
    with pytest.raises(TypeError):
        SymbolLocation(start_line, end_line, start_column, end_column)


def test_rejects_start_line_greater_than_end_line() -> None:
    with pytest.raises(ValueError, match="start_line cannot be greater than end_line."):
        SymbolLocation(16, 10, 2, 5)


def test_rejects_start_column_greater_than_end_column() -> None:
    with pytest.raises(
        ValueError,
        match="start_column cannot be greater than end_column on the same line.",
    ):
        SymbolLocation(7, 7, 7, 2)


def test_symbol_location_is_immutable() -> None:
    start_line = 1
    symbol_location = SymbolLocation(start_line, 1, 3, 5)

    with pytest.raises(FrozenInstanceError):
        symbol_location.start_line = 4
