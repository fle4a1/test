from tortoise import fields
from tortoise.models import Model

from internal.core.types import RolesEnum


class User(Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=30, unique=True)
    password_hash = fields.BinaryField()
    role = fields.CharEnumField(RolesEnum, default=RolesEnum.USER)

    class Meta:
        table = 'users'
