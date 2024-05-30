import click
from internal.core.types import RolesEnum
from internal.core.utils import sync_to_async
from internal.repositories.db.helpers import close_db_connections, init_db
from internal.repositories.db.user import UserRepository


@click.group()
def users():
    pass


@users.command('create_admin')
@click.option('--username', prompt='Имя администратора', help='Какое имя будет у пользователя с правами администратора')
@click.option('--password', prompt='Пароль администратора', help='Пароль администратора')
@sync_to_async
async def create_admin(username: str, password: str) -> None:
    user_repo = UserRepository()

    await init_db()
    await user_repo.create(username, password, RolesEnum.ADMIN)
    await close_db_connections()


if __name__ == '__main__':
    users()
