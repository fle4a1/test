import asyncio
from functools import wraps
from typing import Coroutine

from aiofile import async_open

from bcrypt import gensalt, hashpw
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> bytes:
    return hashpw(password.encode('utf-8'), gensalt())


def check_password(password: str, password_hash: bytes):
    return pwd_context.verify(password, password_hash.decode('utf-8'))


async def write(filepath: str, data: bytes) -> Coroutine[None, Exception, None]:
    """Асинхронно записывает бинарный файл

    Args:
        filepath: Путь к файлу
        data: Содержимое для записи
    """
    async with async_open(filepath, 'wb') as file:
        await file.write(data)


def sync_to_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
