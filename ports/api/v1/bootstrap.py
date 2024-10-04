from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

import settings
from internals.providers.query import DataQueryProvider
from internals.providers.parser import LogsProcessor
from . import (
    routes,
    contracts,
    middlewares,
)


def api(
    rdbs_dsn: str
) -> contracts.Application:
    api_app = contracts.Application()
    api_app = _bootstrap_exception_handlers(api_app)
    api_app = _bootstrap_cors(api_app)
    api_app.include_router(_bootstrap_router())
    api_app.query_provider = DataQueryProvider(rdbs_dsn)
    api_app.logs_processor = LogsProcessor(rdbs_dsn, settings.LOGFILE_PATH)
    return api_app


"""
Историю с CORS можно и нужно разруливать на уровне гейтвея, 
но в данном случае, ввиду отсутствия такового, это сделано в виде middleware
"""


def _bootstrap_cors(api_app: contracts.Application):
    origins = ["*"]

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return api_app


def _bootstrap_router(api_version: str = 'v1'):
    if api_version == 'v1':
        router = routes.v1
        return router


def _bootstrap_exception_handlers(
    api_app: contracts.Application
) -> contracts.Application:
    api_app.add_exception_handler(
        RequestValidationError,
        middlewares.validation_exception_handler
    )
    api_app.add_exception_handler(
        Exception,
        middlewares.generic_exception_handler
    )
    return api_app
