from urllib.parse import quote

import pytest
from httpx import AsyncClient, MockTransport, Response

from internal.repositories.eos_schedule import EosScheduleRepository


def mock_eos_response(request):
    if request.url.path == '/login' and request.method == 'GET':
        return Response(
            200,
            content="""
        <html>
            <input name="logintoken" value="daldasdadadwadwa"/>
        </html>
        """,
        )
    elif request.url.path == '/login' and request.method == 'POST':
        pass
    elif request.url.path == '/schedule' and request.method == 'GET':
        body = """
        <html>
            <a href="http://test.ru/folder/id=11">Schedule 1</a>
            <a href="http://test.ru/folder/id=12">Schedule 2</a>
            <a href="http://test.ru/folder/id=13">Schedule 3</a>
            <a href="http://test.ru/folder/id=14">Schedule 4</a>
        </html>
        """
        return Response(200, content=body)
    elif request.url.path.startswith('/folder/id') and request.method == 'GET':
        body = f'''
        <html>
            <head>
                <title>Расписание занятий</title>
            </head>
            <body>
            <a href="http://test.ru/content/{quote('ИДБ-21-12')}.pdf?forcedownload=1"/>
            <a href="http://test.ru/content/{quote('ИДБ-21-12')}.ctf?forcedownload=1"/>
            <a href="http://test.ru/content/{quote('ИДБ-21-01')}.pdf?forcedownload=1"/>
            </body>
        </html>
        '''
        return Response(200, content=body)
    elif '.pdf' in request.url.path:
        pdf_content = b'%PDF-1.4 mock pdf content'
        return Response(200, content=pdf_content)
    return Response(404)


@pytest.fixture
def mock_eos_client():
    return AsyncClient(transport=MockTransport(mock_eos_response))


@pytest.fixture
async def mock_eos_repository(mock_eos_client):
    repo = await EosScheduleRepository.create(mock_eos_client)
    return repo
