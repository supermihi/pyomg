from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PartialDate:
    year: int
    month: int | None = None
    day: int | None = None

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
