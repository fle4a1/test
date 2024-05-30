from internal.repositories.redis import BaseRedisReposity


class ScheduleVersionRepository(BaseRedisReposity):
    """Репозитория для взаимодействия с версионностью расписаний"""

    store_key = 'schedule'

    async def update_schedule_version(self, data: dict[str, str]) -> int:
        """Изменяет версию расписаний

        Args:
            mapping: словарь формата {ключ:значение}

        Returns:
            int: количество созданных полей
        """
        return await self.client.hset(self.store_key, mapping=data)

    async def get_schedule_version(self) -> dict[str, str]:
        """Возвращает версию расписания в Redis

        Returns:
            dict: словарь формата {ключ:значение}
        """
        return await self.client.hgetall(self.store_key)
