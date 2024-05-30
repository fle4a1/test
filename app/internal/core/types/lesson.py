from datetime import date

from pydantic.dataclasses import dataclass

from internal.core.types import LessonEnum, SubgroupEnum


@dataclass
class Lesson:
    date: date
    time: str
    lesson: str
    professor: str | None
    type: LessonEnum
    subgroup: SubgroupEnum | None
    auditory: str | None
