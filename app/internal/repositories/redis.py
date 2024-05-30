from abc import ABC

from redis.asyncio.client import Redis

import config


class BaseRedisReposity(ABC):
    """Базовый репозиторий для работы с Redis"""

    def __init__(self):
        """Создание пула подключения"""
        self.client = Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
        )
