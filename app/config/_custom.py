import os


# AUTH
SECRET_KEY = NotImplemented
ALGORITHM = NotImplemented
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SUPERTOKEN = NotImplemented

# EOS & Schedule
EOS_URL = NotImplemented
EOS_LOGIN_PATH = NotImplemented
EOS_PATTERN_PATH = NotImplemented
EOS_SCHEDULE_PATH = NotImplemented
EOS_USERNAME = NotImplemented
EOS_PASSWORD = NotImplemented
EOS_SCHEDULE_CHECK_TIME = '03:00'
SCHEDULE_DIR = os.path.normpath(f'{os.path.dirname(__file__)}/../../schedules')

# Postgres
POSTGRES_DB = NotImplemented
POSTGRES_USER = NotImplemented
POSTGRES_PASSWORD = NotImplemented
POSTGRES_HOST = NotImplemented
POSTGRES_PORT = NotImplemented

# Redis
REDIS_HOST = NotImplemented
REDIS_PORT = NotImplemented
REDIS_DB = NotImplemented
