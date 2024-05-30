from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from internal.core.auth import verify_token
from internal.core.exceptions import InvalidTokenException
from internal.services.auth import AuthService


Oauth2SchemeDependency = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='token', auto_error=False))]


def verify_token_dep(token: Oauth2SchemeDependency):
    try:
        return verify_token(token)
    except InvalidTokenException as e:
        raise HTTPException(status_code=401, detail='Invalid token') from e


VerifyTokenDependency = Annotated[str, Depends(verify_token_dep)]

AuthServiceDependency = Annotated[AuthService, Depends(AuthService)]
