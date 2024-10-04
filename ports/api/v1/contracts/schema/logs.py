import datetime

from . import generic


class LogItemResponseData(generic.ResponseData):
    timestamp: datetime.datetime
    message: str


class LogsListResponseModel(generic.PaginatedListResponseModel):
    data: list[LogItemResponseData]


class LogsParsedResponseModel(generic.ResponseModel):
    data: str
