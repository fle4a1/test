import uuid
from typing import Coroutine, Type

from tortoise.exceptions import DoesNotExist, IntegrityError, MultipleObjectsReturned

from internal.core.exceptions import DoesNotExistException, IntegrityException, MultipleObjectsException
from internal.core.types import Empty, RolesEnum
from internal.core.utils import hash_password
from internal.dto.user import UserOut
from internal.repositories.db.base import BaseDBRepository
from internal.repositories.db.models import User


class UserRepository(BaseDBRepository):
    """Репозиторий для работы с пользователем"""

    model = User

    async def get_one(
        self,
        user_id: uuid.UUID | Type[Empty] = Empty,
        username: str | Type[Empty] = Empty,
        role: RolesEnum | Type[Empty] = Empty,
    ) -> Coroutine[None, DoesNotExistException, UserOut]:
        """Получение одного пользователя по фильтрам из таблицы users

        Args:
            user_id: ID пользователя. По умолчанию - Empty.
            username: Имя пользователя. По умолчанию - Empty.
            role: Роль пользователя. По умолчанию - Empty.

        Raises:
            DoesNotExistException: Если пользователя не существует.
            MultipleObjectsException: Если более одного пользователя соответствующего фильтру.

        Returns:
            UserOut: DTO запись пользователя.
        """
        filters = {
            'id': user_id,
            'username': username,
            'role': role,
        }

        filters = {key: value for key, value in filters.items() if value is not Empty}

        try:
            return await UserOut.from_queryset_single(self.model.get(**filters))
        except DoesNotExist as e:
            raise DoesNotExistException() from e
        except MultipleObjectsReturned as e:
            raise MultipleObjectsException() from e

    async def get_many(
        self,
        user_id: uuid.UUID | Type[Empty] = Empty,
        username: str | Type[Empty] = Empty,
        role: RolesEnum | Type[Empty] = Empty,
    ) -> Coroutine[None, Exception, list[UserOut]]:
        """Получение всех пользоватей или определенных пользователей по фильтру
        из таблицы users

        Args:
            user_id: ID пользователя. По умолчанию - Empty.
            username: Имя пользователя. По умолчанию - Empty.
            role: Роль пользователя. По умолчанию - Empty.

        Returns:
            list[UserOut]: Список пользователей.
        """
        filters = {
            'id': user_id,
            'username': username,
            'role': role,
        }

        filters = {key: value for key, value in filters.items() if value is not Empty}
        return await UserOut.from_queryset(self.model.filter(**filters))

    async def create(
        self,
        username: str,
        password: str,
        role: RolesEnum = RolesEnum.USER,
    ) -> Coroutine[None, IntegrityException, UserOut]:
        """Создает нового пользователя с указанными данными.

        Args:
            username: Имя пользователя.
            password: Пароль пользователя.
            role: Роль пользователя. По умолчанию - user.

        Returns:
            UserOut: Cозданный пользователь.

        Raises:
            IntegrityException: Если имя пользователя уже существует.
        """
        data = {
            'username': username,
            'password_hash': hash_password(password),
            'role': role,
        }
        try:
            user = await self.model.create(**data)
            return await UserOut.from_tortoise_orm(user)
        except IntegrityError as e:
            raise IntegrityException() from e

    async def update(
        self,
        user_id: uuid.UUID,
        new_password: str | Type[Empty] = Empty,
        new_role: RolesEnum | Type[Empty] = Empty,
    ) -> Coroutine[None, Exception, int]:
        """Обновляет информацию о пользователе (пароль) по id.

        Args:
            user_id: Идентификатор пользователя.
            new_password: Новый пароль пользователя. По умолчанию - Empty.
            new_role: Новая роль пользователя. По умолчанию - Empty.

        Returns:
            int: количество обновленных пользователей.
        """

        data = {
            'password_hash': hash_password(new_password),
            'role': new_role,
        }
        data = {key: value for key, value in data.items() if value is not Empty}
        return await self.model.filter(id=user_id).update(**data)

    async def delete(
        self,
        user_id: uuid.UUID | Type[Empty] = Empty,
        username: str | Type[Empty] = Empty,
        role: RolesEnum | Type[Empty] = Empty,
    ) -> Coroutine[None, Exception, int]:
        """Удаляет пользователей из таблицы users по параметрам

        Args:
            user_id: Уникальный идентификатор пользователей.
            username: Уникальное имя пользователя.
            role: Роль пользователя.

        Returns:
            int: количество удаленных пользователей
        """
        filters = {
            'id': user_id,
            'username': username,
            'role': role,
        }
        filters = {key: value for key, value in filters.items() if value is not Empty}
        return await self.model.filter(**filters).delete()
