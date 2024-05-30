from tortoise.contrib.pydantic.creator import pydantic_model_creator

from internal.repositories.db.models import Schedule


ScheduleOut = pydantic_model_creator(Schedule, name='ScheduleDTO', exclude=('id',))


class ProfessorScheduleOut(ScheduleOut):
    group: list[str] | str
