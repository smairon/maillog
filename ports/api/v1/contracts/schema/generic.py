import abc
import typing

import pydantic


class ResponseData(pydantic.BaseModel):
    pass


class ErrorResponseData(ResponseData):
    code: int
    message: str
    details: dict | None


class PaginatedListMetaData(ResponseData):
    quantity: int


class ResponseModel(pydantic.BaseModel, abc.ABC):
    data: typing.Any


class ErrorResponseModel(ResponseModel):
    data: ErrorResponseData


class ListResponseModel(ResponseModel):
    data: list[ResponseData]


class PaginatedListResponseModel(ListResponseModel):
    meta: PaginatedListMetaData
