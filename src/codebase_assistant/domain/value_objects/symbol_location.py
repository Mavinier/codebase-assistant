from dataclasses import dataclass, fields


@dataclass(frozen=True)
class SymbolLocation:
    start_line: int
    end_line: int
    start_column: int
    end_column: int

    def __post_init__(self) -> None:
        for position in fields(self):
            value = getattr(self, position.name)

            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"Field '{position.name}' must be an integer.")

            if value < 0:
                raise ValueError(
                    f"Field '{position.name}' must be greater than or equal to 0."
                )

        if self.start_line > self.end_line:
            raise ValueError("start_line cannot be greater than end_line.")

        if self.start_line == self.end_line and self.start_column > self.end_column:
            raise ValueError(
                "start_column cannot be greater than end_column on the same line."
            )
