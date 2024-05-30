import asyncio
from datetime import datetime
from functools import reduce
from typing import Coroutine, Type
from uuid import UUID

from tortoise.exceptions import DoesNotExist, IntegrityError, MultipleObjectsReturned
from tortoise.expressions import Q

from internal.core.exceptions import DoesNotExistException, IntegrityException, MultipleObjectsException
from internal.core.types import Empty, LessonEnum, SubgroupEnum
from internal.dto.schedule import ScheduleOut
from internal.repositories.db.base import BaseDBRepository
from internal.repositories.db.models import Schedule


class ScheduleRepository(BaseDBRepository):
    """Репозиторий для работы с таблицой schedule"""

    model = Schedule

    async def get_one(
        self,
        datetime_start: datetime | Type[Empty] = Empty,
        datetime_end: datetime | Type[Empty] = Empty,
        lesson: str | Type[Empty] = Empty,
        professor: str | None | Type[Empty] = Empty,
        type: LessonEnum | Type[Empty] = Empty,
        subgroup: SubgroupEnum | None | Type[Empty] = Empty,
        auditory: str | None | Type[Empty] = Empty,
        group: str | Type[Empty] = Empty,
    ) -> Coroutine[None, DoesNotExistException, ScheduleOut]:
        """Получение одного занятия по фильтрам из таблицы schedule

        Args:
            datetime_start: Дата и время начала занятий. По умолчанию Empty.
            datetime_end: Дата и время конца занятий. По умолчанию Empty.
            lesson: Название предмета. По умолчанию Empty.
            professor: Преподаватель. По умолчанию Empty.
            type: Тип занятия. По умолчанию Empty.
            subgroup: Подгруппа. По умолчанию Empty.
            auditory: Аудитория. По умолчанию Empty.
            group: Наименование группы. По умолчанию Empty.

        Raises:
            DoesNotExistException: Если занятия нет в СУБД
            MultipleObjectsException: Если более одного занятия соответствующего фильтру
        Returns:
            ScheduleOut: DTO модель записи из таблицы СУБД
        """
        filters = {
            'datetime_start__gte': datetime_start,
            'datetime_end__lte': datetime_end,
            'lesson': lesson,
            'professor': professor,
            'type': type,
            'subgroup': subgroup,
            'auditory': auditory,
            'group': group,
        }
        filters = {key: value for key, value in filters.items() if value is not Empty}
        try:
            return await ScheduleOut.from_queryset_single(self.model.get(**filters))
        except DoesNotExist as e:
            raise DoesNotExistException() from e
        except MultipleObjectsReturned as e:
            raise MultipleObjectsException() from e

    async def get_many(
        self,
        datetime_start: datetime | Type[Empty] = Empty,
        datetime_end: datetime | Type[Empty] = Empty,
        lesson: str | Type[Empty] = Empty,
        professor: str | None | Type[Empty] = Empty,
        type: LessonEnum | Type[Empty] = Empty,
        subgroup: SubgroupEnum | None | Type[Empty] = Empty,
        auditory: str | None | Type[Empty] = Empty,
        group: str | Type[Empty] = Empty,
    ) -> Coroutine[None, Exception, list[ScheduleOut]]:
        """Получение всех занятий из таблицы schedule по фильтру

        Args:
            datetime_start: Дата и время начала занятий. По умолчанию Empty.
            datetime_end: Дата и время конца занятий. По умолчанию Empty.
            lesson: Название предмета. По умолчанию Empty.
            professor: Преподаватель. По умолчанию Empty.
            type: Тип занятия. По умолчанию Empty.
            subgroup: Подгруппа. По умолчанию Empty.
            auditory: Аудитория. По умолчанию Empty.
            group: Наименование группы. По умолчанию Empty.

        Returns:
            list[ScheduleOut]: Список DTO занятий
        """
        filters = {
            'datetime_start__gte': datetime_start,
            'datetime_end__lte': datetime_end,
            'lesson': lesson,
            'professor': professor,
            'type': type,
            'auditory': auditory,
            'group': group,
        }

        filters = (Q(**{key: value}) for key, value in filters.items() if value is not Empty)
        filters = reduce(lambda x, y: x & y, filters)
        if subgroup is not Empty:
            filters &= Q(subgroup=subgroup) | Q(subgroup__isnull=True)
        return await ScheduleOut.from_queryset(self.model.filter(filters))

    async def create(
        self,
        datetime_start: datetime,
        datetime_end: datetime,
        lesson: str,
        professor: str | None,
        type: LessonEnum,
        subgroup: SubgroupEnum | None,
        auditory: str | None,
        group: str,
    ) -> Coroutine[None, IntegrityException, ScheduleOut]:
        """Создание одного занятия в таблице schedule

        Args:
            datetime_start: Дата и время начала занятия.
            datetime_end: Дата и время конца занятия.
            lesson: Название предмета.
            professor: Преподаватель.
            type: Тип занятия.
            subgroup: Подгруппа.
            auditory: Аудитория.
            group: Наименование группы.

        Raises:
            IntegrityException: Если занятие уже есть в таблице

        Returns:
            ScheduleOut: Созданная DTO запись занятия
        """
        data = {
            'datetime_start': datetime_start,
            'datetime_end': datetime_end,
            'lesson': lesson,
            'professor': professor,
            'type': type,
            'subgroup': subgroup,
            'auditory': auditory,
            'group': group,
        }
        try:
            user = await self.model.create(**data)
            return await ScheduleOut.from_tortoise_orm(user)
        except IntegrityError as e:
            raise IntegrityException() from e

    async def create_many(
        self,
        objects: list[dict],
    ) -> Coroutine[None, Exception, list[ScheduleOut]]:
        """Создание множества занятий в таблице schedule

        Args:
            objects: Объекты для создания

        Returns:
            list[ScheduleOut]: список созданных объектов
        """
        schedules = map(lambda x: self.model(**x), objects)
        schedules = await self.model.bulk_create(schedules, ignore_conflicts=True)
        result = await asyncio.gather(*[ScheduleOut.from_tortoise_orm(schedule) for schedule in schedules])
        return result

    async def update(
        self,
        id: UUID,
        datetime_start: datetime | Type[Empty] = Empty,
        datetime_end: datetime | Type[Empty] = Empty,
        lesson: str | Type[Empty] = Empty,
        professor: str | None | Type[Empty] = Empty,
        type: LessonEnum | Type[Empty] = Empty,
        subgroup: SubgroupEnum | None | Type[Empty] = Empty,
        auditory: str | None | Type[Empty] = Empty,
        group: str | Type[Empty] = Empty,
    ) -> Coroutine[None, Exception, int]:
        """Изменение одного расписания в таблице schedule

        Args:
            id: UUID занятия.
            datetime_start: Дата и время начала занятия. По умолчанию Empty.
            datetime_end: Дата и время конца занятия. По умолчанию Empty.
            lesson: Название предмета. По умолчанию Empty.
            professor: Преподаватель. По умолчанию Empty.
            type: Тип занятия. По умолчанию Empty.
            subgroup: Подгруппа. По умолчанию Empty.
            auditory: Аудитория. По умолчанию Empty.
            group: Наименование группы. По умолчанию Empty.

        Returns:
            int: Количество измененных записей
        """
        data = {
            'datetime_start': datetime_start,
            'datetime_end': datetime_end,
            'lesson': lesson,
            'professor': professor,
            'type': type,
            'subgroup': subgroup,
            'auditory': auditory,
            'group': group,
        }
        data = {key: value for key, value in data.items() if value is not Empty}
        return await self.model.filter(id=id).update(**data)

    async def delete(
        self,
        datetime_start: datetime | Type[Empty] = Empty,
        datetime_end: datetime | Type[Empty] = Empty,
        lesson: str | Type[Empty] = Empty,
        professor: str | None | Type[Empty] = Empty,
        type: LessonEnum | Type[Empty] = Empty,
        subgroup: SubgroupEnum | None | Type[Empty] = Empty,
        auditory: str | None | Type[Empty] = Empty,
        group: str | Type[Empty] = Empty,
    ) -> Coroutine[None, Exception, int]:
        """Удаление расписаний по фильтру

        Args:
            datetime_start: Дата и время начала занятий. По умолчанию Empty.
            datetime_end: Дата и время конца занятий. По умолчанию Empty.
            lesson: Название предмета. По умолчанию Empty.
            professor: Преподаватель. По умолчанию Empty.
            type: Тип занятия. По умолчанию Empty.
            subgroup: Подгруппа. По умолчанию Empty.
            auditory: Аудитория. По умолчанию Empty.
            group: Наименование группы. По умолчанию Empty.

        Returns:
            int: Количество удаленных записей
        """
        filters = {
            'datetime_start__gte': datetime_start,
            'datetime_end__lte': datetime_end,
            'lesson': lesson,
            'professor': professor,
            'type': type,
            'subgroup': subgroup,
            'auditory': auditory,
            'group': group,
        }
        filters = {key: value for key, value in filters.items() if value is not Empty}
        return await self.model.filter(**filters).delete()

    async def get_professors(self, professor: str = None) -> list[str]:
        """Получение списка преподавателей по схожести входного параметра

        Args:
            professor: преподаватель. По умолчанию None.

        Returns:
            list: список преподавателей соответствующих фильтру
        """
        if not professor:
            result = await self.model.raw('''SELECT DISTINCT "professor" FROM "schedule"''')
        else:
            result = await self.model.raw(f'''SELECT DISTINCT "professor" FROM "schedule" WHERE "professor" % '{professor}';''')
        return [obj.professor for obj in result if obj.professor is not None]

    async def get_groups(self, group: str = None) -> list[str]:
        """Получение списка групп по схожести входного параметра

        Args:
            group : группа. По умолчанию None

        Returns:
            list: список групп соответствующих фильтру
        """
        if not group:
            result = await self.model.raw('''SELECT DISTINCT "group" FROM "schedule"''')
        else:
            result = await self.model.raw(f'''SELECT DISTINCT "group" FROM "schedule" WHERE "group" % '{group}';''')
        return [obj.group for obj in result]
