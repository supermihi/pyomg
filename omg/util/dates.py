from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PartialDate:
    year: int
    month: int | None = None
    day: int | None = None

    def __str__(self):
        if self.month is None:
            return str(self.year)
        if self.day is None:
            return f'{self.year}-{self.month}'
        return f'{self.year}-{self.month}-{self.day}'

    @staticmethod
    def parse(date: str):
        parts = date.split('-')
        if len(parts) == 1:
            return PartialDate(int(parts[0]))
        if len(parts) == 2:
            return PartialDate(int(parts[0]), int(parts[1]))
        if len(parts) == 3:
            return PartialDate(int(parts[0]), int(parts[1]), int(parts[2]))
        raise ValueError(f'invalid PartialDate format: {date}')
