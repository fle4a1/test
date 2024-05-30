import os
from datetime import datetime

from pydantic import RootModel
from schedule_parser import Parser
from schedule_parser.schemas.lesson import Lesson

import config
from external.repositories.scheduleVersion import ScheduleVersionRepository
from internal.repositories.db.schedule import ScheduleRepository
from internal.repositories.eos_schedule import EosScheduleRepository


async def fetch_urls() -> None:
    """Задача на скачивание новых расписаний и загрузку их в БД"""

    repo = await EosScheduleRepository.create()
    urls = await repo.get_urls()
    groups = map(lambda x: x.replace('.pdf', ''), repo.get_filenames(urls))
    group_link = dict(zip(groups, urls))
    if result := await get_changed_urls(group_link):
        await repo.load_schedule_files(result.values())
        await process_schedules(result.keys())
    await repo.cleanup()


async def get_changed_urls(urls: dict[str, str]) -> dict[str, str]:
    """Проверяет изменение ссылок на скачивании в сравнении с прошлым запросом

    Args:
        urls: Словарь актуальных значений группа: ссылка

    Returns:
        dict: Словавь групп и ссылок, для которых изменилось расписание
    """
    repo = ScheduleVersionRepository()
    redis_data = await repo.get_schedule_version()
    result = {}
    for key, value in urls.items():
        if key not in redis_data or redis_data[key] != value:
            result.update({key: value})
    await repo.update_schedule_version(result)
    return result


async def process_schedules(groups: list[str]) -> None:
    """Парсит переданные группы и записывает их в СУБД

    Args:
        groups: Список групп
    """
    repo = ScheduleRepository()
    current_datetime = datetime.today()
    parser = Parser()
    for group in groups:
        parser.read(os.path.join(config.SCHEDULE_DIR, f'{group}.pdf'))
        lessons = process_lessons(parser.parse(), current_datetime)
        await repo.delete(datetime_start=current_datetime, group=group)
        await repo.create_many(lessons)


def process_lessons(lessons: list[Lesson], current_datetime: datetime) -> dict:
    """Преобразует занятия которые еще не были проведены в словарь

    Args:
        lessons: Список занятий
        current_datetime: Текущая дата

    yield:
        dict: Словарь занятия
    """
    for lesson in lessons:
        if lesson.datetime_start >= current_datetime:
            yield RootModel[Lesson](lesson).model_dump()
