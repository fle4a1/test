from fastapi import APIRouter

from internal.api.status import STATUS_ROUTER
from internal.api.v1 import V1_ROUTER


API_ROUTER = APIRouter(prefix='/api')
API_ROUTER.include_router(STATUS_ROUTER)
API_ROUTER.include_router(V1_ROUTER)
