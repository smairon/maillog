from .bootstrap import v1
from ..contracts import schema
from ..endpoints import logs
from .generic import response_schema

TAGS = ['Logs']

v1.add_api_route(
    path='/logs',
    endpoint=logs.roster,
    responses=response_schema(schema.logs.LogsListResponseModel, 422, 500),
    methods=['GET'],
    tags=TAGS
)

v1.add_api_route(
    path='/logs',
    endpoint=logs.parse,
    responses=response_schema(schema.logs.LogsParsedResponseModel, 422, 500),
    methods=['POST'],
    tags=TAGS
)
