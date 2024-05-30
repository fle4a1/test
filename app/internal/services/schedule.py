from datetime import datetime
from typing import Type

from internal.core.types import Empty, SubgroupEnum
from internal.dto.schedule import ProfessorScheduleOut, ScheduleOut
from internal.repositories.db.schedule import ScheduleRepository


class ScheduleService:
    def __init__(self, repo: ScheduleRepository):
        self.repo = repo

    async def get_schedule(
        self,
        group: str | Type[Empty] = Empty,
        professor: str | None | Type[Empty] = Empty,
        datetime_start: datetime | Type[Empty] = Empty,
        datetime_end: datetime | Type[Empty] = Empty,
        subgroup: SubgroupEnum | None | Type[Empty] = Empty,
    ) -> list[ScheduleOut]:
        """Получение занятий по фильтру

        Args:
            group: группа. По умолчанию Empty.
            professor: данные преподавателя. По умолчанию Empty.
            datetime_start: дата начала занятий. По умолчанию Empty.
            datetime_end: дата конца занятий. По умолчанию Empty.
            subgroup: буква подгруппы. По умолчанию Empty.

        Returns:
            list[ScheduleOut]: список занятий соответствующий фильтру
        """
        result = await self.repo.get_many(
            group=group,
            professor=professor,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            subgroup=subgroup,
        )
        return result

    async def get_professor_schedule(
        self,
        professor: str | None | Type[Empty] = Empty,
        datetime_start: datetime | Type[Empty] = Empty,
        datetime_end: datetime | Type[Empty] = Empty,
        subgroup: SubgroupEnum | None | Type[Empty] = Empty,
    ) -> list[ProfessorScheduleOut]:
        """Получение занятий конкретного преподавателя по фильтру

        Args:
            professor: данные преподавателя. По умолчанию Empty.
            datetime_start: дата начала занятий. По умолчанию Empty.
            datetime_end: дата конца занятий. По умолчанию Empty.
            subgroup: буква подгруппы. По умолчанию Empty.

        Returns:
            list[ScheduleOut]: список занятий соответствующий фильтру
        """
        result = await self.repo.get_many(
            professor=professor,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            subgroup=subgroup,
        )

        unified_lessons = {}
        for item in result:
            if item.datetime_start not in unified_lessons.keys():
                unified_lessons[item.datetime_start] = item.dict()
                unified_lessons[item.datetime_start]['group'] = [item.group]
            else:
                unified_lessons[item.datetime_start]['group'].append(item.group)
        unified_lessons = dict(sorted(unified_lessons.items())).values()

        return [ProfessorScheduleOut.model_validate(item) for item in unified_lessons]

    async def get_groups(
        self,
        similar: str = None,
    ) -> list[str]:
        """Получение похожих групп

        Args:
            similar: группа для поиска. Изначально None.

        Returns:
            list[str]: список групп которые схожи с исходным
        """
        return await self.repo.get_groups(group=similar)

    async def get_professors(
        self,
        similar: str = None,
    ) -> list[str]:
        """Получение похожих преподавателей

        Args:
            similar: преподаватель для поиска. Изначально None.

        Returns:
            list[str]: список преподавателей схожих с исходным запросом
        """
        return await self.repo.get_professors(professor=similar)
