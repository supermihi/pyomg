from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Recording:
    mbid: str


@dataclass(frozen=True)
class Work:
    mbid: str


@dataclass(frozen=True)
class Artist:
    mbid: str


@dataclass(frozen=True)
class Performance:
    """Work-recording relation."""
    recording: Recording
    work: Work

    @staticmethod
    def from_work_relation(recording: Recording, work_relation: dict) -> Performance:
        """Create a Performance from a work-relation JSON object."""
        return Performance(work=Work(work_relation['work']['id']), recording=recording)


@dataclass(frozen=True)
class WorkPart:
    enclosing_work: Work
    part: Work
    number: int

    @staticmethod
    def from_work_relation(work: Work, work_relation: dict) -> WorkPart:
        return WorkPart(
            enclosing_work=Work(work_relation['work']['id']),
            part=work,
            number=int(work_relation['ordering-key'])
        )
