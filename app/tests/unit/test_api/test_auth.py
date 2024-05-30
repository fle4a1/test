import pytest

from internal.core.auth import encode_access_token


@pytest.mark.asyncio
async def test_status_route_with_token_and_with_debug(client, mocker):
    mocker.patch('config.DEBUG', True)
    username = 'test'
    valid_token = encode_access_token(username)
    response = client.get('api/v1/status', headers={'Authorization': f'Bearer {valid_token}'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Hey there, DEBUG'}


@pytest.mark.asyncio
async def test_status_route_with_token_and_without_debug(client, mocker):
    mocker.patch('config.DEBUG', False)
    username = 'test'
    valid_token = encode_access_token(username)
    response = client.get('api/v1/status', headers={'Authorization': f'Bearer {valid_token}'})
    assert response.status_code == 200
    assert response.json() == {'message': f'Hey there, {username}'}


@pytest.mark.asyncio
async def test_status_route_without_token_and_with_debug(client, mocker):
    mocker.patch('config.DEBUG', True)
    response = client.get('api/v1/status')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hey there, DEBUG'}


@pytest.mark.asyncio
async def test_status_route_without_token_and_without_debug(client, mocker):
    mocker.patch('config.DEBUG', False)
    response = client.get('api/v1/status')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid token'}


@pytest.mark.asyncio
async def test_status_route_invalid_token_with_debug(client, mocker):
    mocker.patch('config.DEBUG', True)
    invalid_token = 'Invalid token'
    response = client.get('api/v1/status', headers={'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Hey there, DEBUG'}


@pytest.mark.asyncio
async def test_status_route_with_invalid_token_without_debug(client, mocker):
    mocker.patch('config.DEBUG', False)
    invalid_token = 'Invalid token'
    response = client.get('api/v1/status', headers={'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid token'}
