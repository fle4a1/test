from typing import Annotated

from fastapi import Depends

from internal.repositories.db.schedule import ScheduleRepository
from internal.services.schedule import ScheduleService


ScheduleRepositoryDependency = Annotated[ScheduleRepository, Depends(ScheduleRepository)]


def schedule_service_dep(repo: ScheduleRepositoryDependency):
    return ScheduleService(repo=repo)


ScheduleServiceDependency = Annotated[ScheduleService, Depends(schedule_service_dep)]
