import os

import pytest
from aiofile import async_open

from internal.core.utils import write


@pytest.mark.asyncio
async def test_write(tmp_path):
    data = b'example'
    filepath = f'{tmp_path}/ИДБ-21-111.pdf'
    await write(filepath, data)
    assert os.path.exists(filepath)
    async with async_open(filepath, 'rb') as file:
        assert await file.read() == data
