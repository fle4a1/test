from fastapi import APIRouter

from internal.dependencies.auth import VerifyTokenDependency


STATUS_ROUTER = APIRouter()


@STATUS_ROUTER.get('/status')
async def status_handler(username: VerifyTokenDependency):
    return {'message': f'Hey there, {username}'}
