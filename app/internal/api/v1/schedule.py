from typing import Annotated

from fastapi import APIRouter, Depends

from internal.api.v1.schemas.request.schedule import ScheduleRequest, SimilarRequest
from internal.api.v1.schemas.response.schedule import GroupResponse, ProfessorResponse, ProfessorScheduleResponse, ScheduleResponse
from internal.dependencies.auth import verify_token_dep
from internal.dependencies.schedule import ScheduleServiceDependency


SCHEDULE_ROUTER = APIRouter(dependencies=[Depends(verify_token_dep)])


@SCHEDULE_ROUTER.get('/schedule')
async def get_schedule(
    request_data: Annotated[ScheduleRequest, Depends(ScheduleRequest)],
    service: ScheduleServiceDependency,
) -> ScheduleResponse:
    schedule_data = await service.get_schedule(**request_data.model_dump(exclude_defaults=True))
    return ScheduleResponse(schedule=schedule_data)


@SCHEDULE_ROUTER.get('/professor_schedule')
async def get_professor_schedule(
    request_data: Annotated[ScheduleRequest, Depends(ScheduleRequest)],
    service: ScheduleServiceDependency,
) -> ProfessorScheduleResponse:
    professor_schedule_data = await service.get_professor_schedule(**request_data.model_dump(exclude_defaults=True))
    return ProfessorScheduleResponse(professor_schedule=professor_schedule_data)


@SCHEDULE_ROUTER.get('/group')
async def get_groups(
    requests_data: Annotated[SimilarRequest, Depends(SimilarRequest)],
    service: ScheduleServiceDependency,
) -> GroupResponse:
    groups_data = await service.get_groups(**requests_data.model_dump(exclude_defaults=True))
    return GroupResponse(groups=groups_data)


@SCHEDULE_ROUTER.get('/professor')
async def get_professors(
    request_data: Annotated[SimilarRequest, Depends(SimilarRequest)],
    service: ScheduleServiceDependency,
) -> ProfessorResponse:
    professors_data = await service.get_professors(**request_data.model_dump(exclude_defaults=True))
    return ProfessorResponse(professors=professors_data)
