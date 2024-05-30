from tortoise import Tortoise

import config


def create_db_url():
    return 'postgres://{}:{}@{}:{}/{}'.format(config.POSTGRES_USER, config.POSTGRES_PASSWORD, config.POSTGRES_HOST, config.POSTGRES_PORT, config.POSTGRES_DB)


TORTOISE_ORM_CONFIG = {
    'connections': {'default': create_db_url()},
    'apps': {
        'default': {
            'models': ['internal.repositories.db.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}


async def init_db():
    await Tortoise.init(TORTOISE_ORM_CONFIG)


async def close_db_connections():
    await Tortoise.close_connections()
