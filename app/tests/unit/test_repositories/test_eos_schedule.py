import os
from random import randint
from unittest.mock import patch
from urllib.parse import quote

import pytest

from internal.repositories.eos_schedule import EosScheduleRepository


@pytest.mark.asyncio
async def test_get_urls(mock_eos_repository):
    expected_results = [f"http://test.ru/content/{quote('ИДБ-21-12')}.pdf?forcedownload=1", f"http://test.ru/content/{quote('ИДБ-21-01')}.pdf?forcedownload=1"]
    test_results = await mock_eos_repository.get_urls()
    assert test_results
    for test, expected in zip(test_results, expected_results):
        assert test == expected


@pytest.mark.asyncio
async def test_get_logintoken(mock_eos_repository):
    expected = 'daldasdadadwadwa'
    test = await mock_eos_repository._get_logintoken()
    assert test == expected


@pytest.mark.asyncio
async def test_get_pdf_links(mock_eos_repository):
    links = [
        'http://test.ru/folder/id=11',
        'http://test.ru/folder/id=12',
        'http://test.ru/folder/id=13',
        'http://test.ru/folder/id=14',
    ]
    for link in links:
        result = await mock_eos_repository._get_pdf_links(link)
        assert result
        for pdf_link in result:
            assert '.pdf' in pdf_link


@pytest.mark.asyncio
async def test_load_schedule_files(mock_eos_repository, tmp_path):
    expected_exists_files = ['ИДБ-21-12.pdf', 'ИДБ-21-01.pdf']
    with patch('config.SCHEDULE_DIR', tmp_path):
        links = await mock_eos_repository.get_urls()
        result = await mock_eos_repository.load_schedule_files(links)
        assert result is None
        for file in expected_exists_files:
            assert os.path.exists(f'{tmp_path}/{file}')


def test_get_filenames():
    expected_filenames = ['ИДБ-21-12', 'АДБ-21-02', 'АДМ-21-02' 'ЭДБ-21-05', 'МДБ-21-02', 'МДС-21-03', 'АСП-21-01(27)', 'АСП-21-01(09-5)', 'ИДМ-23-03(ПриМ)']
    links = []
    for filename in expected_filenames:
        id = randint(10000, 40000)
        link = f"https://example.com/everything/{id}/{quote(filename) + '.pdf'}?forcedownload=1"
        links.append(link)
    test_filenames = EosScheduleRepository.get_filenames(links)
    for test, expected in zip(test_filenames, expected_filenames):
        assert test == expected + '.pdf'
