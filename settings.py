import os

APP_HOST = '0.0.0.0'
APP_PORT = 80
APP_WORKERS_NUM = 1

BASE_DIR = os.path.dirname(__file__)
MIGRATION_DIR = os.path.join(BASE_DIR, 'ports/rdbs/migrations')
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGFILE_PATH = os.path.join(DATA_DIR, 'mail.log')

RDBS_DB_NAME = "maillog"

OPENED_PATHS = (
    '/docs',
    '/openapi.json'
)

API_PATH_V1 = "/api/v1"
