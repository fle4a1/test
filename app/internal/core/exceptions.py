from uuid import uuid4


class AppException(Exception):
    msg: str | None = NotImplemented
    error_code = 1
    module_code = 'APP'
    system_prefix: str | None = NotImplemented
    status_code: int = NotImplemented

    def __init__(self, msg='', value=None, cause=None, extra_data=None):
        super().__init__()
        self.msg = msg or self.msg
        self.value = value
        self.cause = cause
        self.extra_data = extra_data
        self.uuid = uuid4()

    def __str__(self):
        return self.msg or self.__doc__ or self.__class__.__name__

    def __call__(self):
        return str(self)

    @classmethod
    def full_code(cls):
        return f'{cls.system_prefix}.{cls.module_code}.{cls.error_code:0>5}'


class UnknownException(AppException):
    system_prefix = 'APP'
    msg = 'Service error'
    error_code = 1
    status_code = 500


class TortoiseModelException(AppException):
    """Класс TortoiseModelException кастомное исключение,
    Является родительскуим, объединяет в себе исключения
    для моделей.

    Args:
        system_prefix: Классификация ряда ошибок.
    """

    system_prefix = 'MODELS'


class IntegrityException(TortoiseModelException):
    """Класс IntegrityException кастомное исключение,
    поднимается при нарушении целостности при создании объекта.

     Args:
        msg: сообщение об ошибке.
        error_code: уникальный идентификатор ошибки.
        status_code: статус код ошибки
    """

    msg = 'Object with this name already exists'
    error_code = 2
    status_code = 409


class DoesNotExistException(TortoiseModelException):
    """Класс DoesNotExistException кастомное исключение,
    поднимается при отсутствии запрашиваемого объекта.

     Args:
        msg: сообщение об ошибке.
        error_code: уникальный идентификатор ошибки.
        status_code: статус код ошибки
    """

    msg = 'Object does not exist'
    error_code = 3
    status_code = 400


class MultipleObjectsException(TortoiseModelException):
    """Кастомное исключение, вызывается если вместо 1 объекта было получено более

    Args:
       msg: сообщение об ошибке.
       error_code: уникальный идентификатор ошибки.
       status_code: статус код ошибки
    """

    msg = 'Multiple objects returned, expected exactly one'
    error_code = 4
    status_code = 400


class AuthException(AppException):
    system_prefix = 'AUTH'


class InvalidTokenException(AuthException):
    msg = 'Token is invalid'
    error_code = 4
    status_code = 401
