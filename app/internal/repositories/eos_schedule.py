from __future__ import annotations

import asyncio
import os
from typing import Coroutine
from urllib.parse import unquote, urljoin, urlparse

from bs4 import BeautifulSoup
from httpx import AsyncClient

import config
from internal.core.utils import write


class EosScheduleRepository:
    """Репозиторий отвечающий за загрузку и работу с расписаниями"""

    EOS_LOGIN_URL = urljoin(config.EOS_URL, config.EOS_LOGIN_PATH)
    EOS_SCHEDULE_URL = urljoin(config.EOS_URL, config.EOS_SCHEDULE_PATH)
    EOS_PATTERN_URL = urljoin(config.EOS_URL, config.EOS_PATTERN_PATH)

    @classmethod
    async def create(cls, session: AsyncClient = None) -> EosScheduleRepository:
        """Фабрика для создания экземпляра репозитория. Также производит авторизацию в эосе

        Args:
            session: Асинхронная сессия для репозитория. По умолчанию None.

        Returns:
            ScheduleRepository: Сущность репозитория
        """
        instance = cls(session)
        params = {'username': config.EOS_USERNAME, 'password': config.EOS_PASSWORD, 'logintoken': await instance._get_logintoken()}
        await instance._session.post(instance.EOS_LOGIN_URL, data=params)
        return instance

    def __init__(self, session: AsyncClient = None) -> None:
        """Инициализирует асинхронную сессию для запросов"""
        self._session = session if session else AsyncClient()

    async def get_urls(self) -> Coroutine[None, Exception, list[str]]:
        """Получает все ссылки со страницы EOS_SCHEDULE_URL для скачивания .pdf файлов расписания

        Returns:
            Список ссылок
        """
        response = await self._session.get(self.EOS_SCHEDULE_URL)
        soup = BeautifulSoup(response.text, 'lxml')
        links = []
        for tag in soup.find_all('a', href=True):
            if tag['href'].startswith(self.EOS_PATTERN_URL):
                links.append(tag['href'])

        pdf_link_tasks = []
        for link in links:
            pdf_link_tasks.append(self._get_pdf_links(link))

        download_links = []
        for result in await asyncio.gather(*pdf_link_tasks):
            download_links.extend(result)

        return download_links

    async def load_schedule_files(self, download_links: list[str]) -> Coroutine[None, Exception, None]:
        """Скачивает все файлы на основе входящих ссылок в SCHEDULE_DIR

        Args:
            download_links: Ссылки на скачивание

        Returns:
            Ничего
        """
        download_tasks = []
        for link in download_links:
            download_tasks.append(self._session.get(link))
        responses = await asyncio.gather(*download_tasks)
        filenames = self.get_filenames(download_links)
        write_tasks = []
        for filename, response in zip(filenames, responses):
            write_tasks.append(write(f'{config.SCHEDULE_DIR}/{filename}', response.content))

        await asyncio.gather(*write_tasks)

    async def _get_logintoken(self) -> Coroutine[None, Exception, str]:
        """Получает логин авторизации из запроса на EOS_LOGIN_URL

        Returns:
            Строка содержающую логин авторизации
        """
        response = await self._session.get(self.EOS_LOGIN_URL)
        soup = BeautifulSoup(response.text, 'lxml')
        logintoken = soup.find('input', {'name': 'logintoken'})['value']
        return logintoken

    async def _get_pdf_links(self, url: str) -> Coroutine[None, Exception, list[str]]:
        """Получает ссылки на загрузку pdf файлов по заданному url

        Args:
            url: Ссылка в виде строки на которую будет производиться запрос

        Returns:
            Список ссылок на загрузку pdf файлов
        """
        response = await self._session.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        if 'экзамен' in str(soup.head.title).lower():
            return []
        links = []
        for tag in soup.find_all('a', href=True):
            if '.pdf' in tag['href']:
                links.append(tag['href'])
        return links

    @staticmethod
    def get_filenames(links: list) -> list[str]:
        """Достает из url ссылок имена файлов

        Args:
            links: Список ссылок, из которых необходимо извлечь название файла

        Returns:
            Список имен файлов
        """
        filenames = []
        for link in links:
            path = urlparse(link).path
            filename = unquote(os.path.basename(path))
            filenames.append(filename)
        return filenames

    async def cleanup(self) -> Coroutine[None, Exception, None]:
        """Асинхронно завершает текущую сессию"""
        await self._session.aclose()
