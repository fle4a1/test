from typing import Annotated

from fastapi import APIRouter, Depends

from internal.api.v1.schemas.request.user import CreateRequest, GetDeleteRequest, UpdateRequest
from internal.dependencies.user import UserServiceDependency, verify_supertoken
from internal.dto.user import UserOut


USER_ROUTER = APIRouter()


@USER_ROUTER.get('/user')
async def get_user(
    request_data: Annotated[GetDeleteRequest, Depends(GetDeleteRequest)],
    service: UserServiceDependency,
) -> UserOut:
    user = await service.get_user(**request_data.model_dump(exclude_defaults=True))

    return user


@USER_ROUTER.post('/user')
async def create_user(
    supertoken: Annotated[str, Depends(verify_supertoken)],
    request_data: CreateRequest,
    service: UserServiceDependency,
) -> UserOut:
    user = await service.create_user(**request_data.model_dump(exclude_defaults=True))

    return user


@USER_ROUTER.patch('/user')
async def update_user(
    request_data: UpdateRequest,
    service: UserServiceDependency,
) -> int:
    return await service.update_user(**request_data.model_dump(exclude_defaults=True))


@USER_ROUTER.delete('/user')
async def delete_user(
    request_data: GetDeleteRequest,
    service: UserServiceDependency,
) -> int:
    return await service.delete_user(**request_data.model_dump(exclude_defaults=True))
