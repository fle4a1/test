from fastapi import APIRouter

from internal.api.v1.auth import AUTH_ROUTER
from internal.api.v1.schedule import SCHEDULE_ROUTER
from internal.api.v1.status import STATUS_ROUTER
from internal.api.v1.user import USER_ROUTER


V1_ROUTER = APIRouter(prefix='/v1')
V1_ROUTER.include_router(STATUS_ROUTER)
V1_ROUTER.include_router(AUTH_ROUTER)
V1_ROUTER.include_router(SCHEDULE_ROUTER)
V1_ROUTER.include_router(USER_ROUTER)
