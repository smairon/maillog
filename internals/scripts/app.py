import os

import uvicorn

import ports
import settings


def api_run():
    host = os.environ.get('APP_HOST') or settings.APP_HOST
    port = int(os.environ.get('APP_PORT')) if os.environ.get('APP_PORT') else settings.APP_PORT
    workers_num = int(os.environ.get('WORKERS_NUM')) if os.environ.get('WORKERS_NUM') else settings.APP_WORKERS_NUM
    uvicorn.run(
        app=ports.api.v1.app,
        host=host,
        port=port,
        workers=workers_num,
        proxy_headers=True,
        reload=os.environ.get('RELOAD') or False,
    )
