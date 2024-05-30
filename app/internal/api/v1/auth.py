from fastapi import APIRouter

from internal.api.v1.schemas.request.auth import LoginRequest
from internal.api.v1.schemas.response.auth import LoginResponse
from internal.dependencies.auth import AuthServiceDependency


AUTH_ROUTER = APIRouter()


@AUTH_ROUTER.post('/login')
async def login_router(request_data: LoginRequest, service: AuthServiceDependency) -> LoginResponse:
    data = await service.login(**request_data.model_dump())
    return LoginResponse(access_token=data)
