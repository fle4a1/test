from fastapi import HTTPException

from internal.core.auth import encode_access_token
from internal.core.utils import check_password
from internal.repositories.db.user import UserRepository


class AuthService:
    """Cервис для аутентификации пользователей"""

    def __init__(self):
        self.repository = UserRepository()

    async def login(self, login: str, password: str) -> str:
        """Функция авторизации, генерирует jwt токен

        Args:
            login: логин для входа (username)
            password: пароль для входа

        Returns:
            str: jwt token
        """

        if user := await self.repository.get_one(username=login):
            if check_password(password, user.password_hash):
                return encode_access_token(login)
        raise HTTPException(status_code=403, detail='Invalid credentials')
