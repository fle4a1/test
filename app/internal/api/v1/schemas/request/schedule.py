from datetime import datetime

from pydantic import BaseModel

from internal.core.types import SubgroupEnum


class ScheduleRequest(BaseModel):
    group: str | None = None
    professor: str | None = None
    datetime_start: datetime | None = None
    datetime_end: datetime | None = None
    subgroup: SubgroupEnum | None = None


class SimilarRequest(BaseModel):
    similar: str | None = None
