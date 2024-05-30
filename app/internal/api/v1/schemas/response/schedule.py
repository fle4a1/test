from pydantic import BaseModel

from internal.dto.schedule import ProfessorScheduleOut, ScheduleOut


class ScheduleResponse(BaseModel):
    schedule: list[ScheduleOut]


class ProfessorScheduleResponse(BaseModel):
    professor_schedule: list[ProfessorScheduleOut]


class GroupResponse(BaseModel):
    groups: list[str]


class ProfessorResponse(BaseModel):
    professors: list[str]
