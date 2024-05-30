from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import config
from external.scheduler.helpers import REDIS_CONFIG
from external.scheduler.tasks import fetch_urls


def apscheduler_init() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_jobstore(RedisJobStore(**REDIS_CONFIG))
    scheduler.add_executor(AsyncIOExecutor())
    hour, minute = map(int, config.EOS_SCHEDULE_CHECK_TIME.split(':'))
    scheduler.add_job(fetch_urls, CronTrigger(hour=hour, minute=minute))
    return scheduler
