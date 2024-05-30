import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

import config
from internal.api import API_ROUTER
from internal.core.exception_handlers import app_exception_handler, http_exception_handler, request_validation_exception_handler, unknown_exception_handler
from internal.core.exceptions import AppException
from internal.core.logs.log_record_factory import LogRecordFactory
from internal.core.middlewares import AddHeaderMiddleware, LoggingMiddleware
from internal.core.settings.validators import validate_config
from internal.repositories.db.helpers import close_db_connections, init_db


def add_routers(app: FastAPI):
    app.include_router(API_ROUTER, prefix=config.APP_URL_PREFIX)


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, unknown_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)


def add_middlewares(app: FastAPI):
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(AddHeaderMiddleware)


@asynccontextmanager
async def initialize(app: FastAPI):
    validate_config(config)
    await init_db()
    yield
    await close_db_connections()


def logging_initialize():
    log_record_factory = LogRecordFactory(logging.getLogRecordFactory())
    logging.setLogRecordFactory(log_record_factory)


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=initialize,
        docs_url=f'{config.APP_URL_PREFIX}/docs',
        redoc_url=f'{config.APP_URL_PREFIX}/redocs',
        openapi_url=f'{config.APP_URL_PREFIX}/openapi.json',
    )
    add_middlewares(app)
    add_exception_handlers(app)
    add_routers(app)
    logging_initialize()
    return app
