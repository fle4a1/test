from tortoise.contrib.pydantic.creator import pydantic_model_creator

from internal.repositories.db.models import User


UserOut = pydantic_model_creator(User, name='UserDTO', exclude=('password_hash',))
