from unittest.mock import AsyncMock, patch

import pytest


MOCKED_DATA = [
    {'group': 'Group1', 'professor': 'Professor1', 'datetime_start': '2024-01-15T08:00:00'},
    {'group': 'Group2', 'professor': 'Professor2', 'datetime_end': '2024-01-16T08:00:00'},
]


async def mock_get_schedule(*args, **kwargs):
    return MOCKED_DATA


@pytest.mark.asyncio
@patch('internal.repositories.db.schedule.ScheduleRepository.get_many', new=AsyncMock(side_effect=mock_get_schedule))
def test_get_schedule_with_params(client, mocker):
    mocker.patch('config.DEBUG', True)
    response = client.get('api/v1/schedule', params={'group': 'Group1', 'professor': 'Professor1'})
    assert response.status_code == 200
    data = response.json()
    assert data['schedule'] == MOCKED_DATA


@pytest.mark.asyncio
@patch('internal.repositories.db.schedule.ScheduleRepository.get_many', new=AsyncMock(side_effect=mock_get_schedule))
def test_get_schedule_without_params(client, mocker):
    mocker.patch('config.DEBUG', True)
    response = client.get('api/v1/schedule')
    assert response.status_code == 200
    data = response.json()
    assert data['schedule'] == MOCKED_DATA
