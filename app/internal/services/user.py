from typing import Type
from uuid import UUID

from internal.core.types import Empty, RolesEnum
from internal.dto.user import UserOut
from internal.repositories.db.user import UserRepository


class UserService:
    """Сервис для взаимодействия с пользователями"""

    def __init__(self):
        self.repo = UserRepository()

    async def create_user(
        self,
        username: str,
        password: str,
        role: RolesEnum = RolesEnum.USER,
    ) -> UserOut:
        """Функция создания пользователя в базе данных

        Args:
            username: логин пользователя
            password: пароль пользователя
            role: роль пользователя. По умолчанию user

        Returns:
            UserOut: пользователь созданный в базе данных
        """
        return await self.repo.create(
            username=username,
            password=password,
            role=role,
        )

    async def get_user(
        self,
        user_id: UUID | Type[Empty] = Empty,
        username: str | Type[Empty] = Empty,
        role: RolesEnum | Type[Empty] = Empty,
    ) -> UserOut:
        """Функция получение первого пользователя соответствующего параметрам

        Args:
            user_id: уникальный идентификатор пользователя. По умолчанию Empty.
            username: логин пользователя. По умолчанию Empty.
            role: роль пользователя. По умолчанию Empty.

        Returns:
            UserOut: пользователь соответствующий запросу
        """
        return await self.repo.get_one(
            user_id=user_id,
            username=username,
            role=role,
        )

    async def update_user(
        self,
        user_id: UUID,
        new_password: str | type[Empty] = Empty,
        new_role: RolesEnum | type[Empty] = Empty,
    ) -> int:
        """Функция обновления данных пользователя

        Args:
            user_id: уникальный идентификатор пользователя.
            new_password: новый пароль для пользователя. По умолчанию Empty.
            new_role: новая роль для пользователя. По умолчанию Empty.

        Returns:
            int: количество обновленных пользователей
        """
        return await self.repo.update(
            user_id=user_id,
            new_password=new_password,
            new_role=new_role,
        )

    async def delete_user(
        self,
        user_id: UUID | type[Empty] = Empty,
        username: str | type[Empty] = Empty,
        role: RolesEnum | type[Empty] = Empty,
    ) -> int:
        """Функция удаление пользователя из базы данных

        Args:
            user_id: уникальный идентификатор пользователя. По умолчанию Empty.
            username: логин пользователя. По умолчанию Empty.
            role: роль пользователя. По умолчанию Empty.

        Returns:
            int: количество удаленных пользователей
        """
        return await self.repo.delete(
            user_id=user_id,
            username=username,
            role=role,
        )
