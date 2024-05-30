import sys
import asyncio
from os import cpu_count
import uvicorn

import config
from config.logging import LOGGING
from external.scheduler.initializer import apscheduler_init
from internal.repositories.db.helpers import close_db_connections, init_db


def run_scheduler():
    scheduler = apscheduler_init()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_db())
    scheduler.start()
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
        loop.run_until_complete(close_db_connections())


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'scheduler':
        run_scheduler()
    elif len(sys.argv) > 1 and sys.argv[1] != 'scheduler':
        raise ValueError('Неизвестный аргумент')
    else:
        uvicorn.run(
            'initializer:create_app',
            factory=True,
            access_log=True,
            log_config=LOGGING,
            reload=config.APP_AUTORELOAD,
            workers=cpu_count(),
            host=config.SERVER_HOST,
            port=config.SERVER_PORT,
        )


if __name__ == '__main__':
    main()
