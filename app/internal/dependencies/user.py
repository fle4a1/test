from typing import Annotated

from fastapi import Depends

import config
from internal.core.exceptions import InvalidTokenException
from internal.services.user import UserService


UserServiceDependency = Annotated[UserService, Depends(UserService)]


def verify_supertoken(token: str):
    if token != config.SUPERTOKEN:
        raise InvalidTokenException()
