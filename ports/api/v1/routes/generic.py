import typing

from ..contracts.schema.generic import ResponseModel, ErrorResponseModel


class ResponseParam(typing.TypedDict):
    model: typing.Any


class RouteParams(typing.TypedDict, total=False):
    path: str
    endpoint: typing.Callable
    methods: typing.Sequence[str]
    tags: typing.Sequence[str]
    status_code: int
    responses: typing.Optional[typing.Dict[
        int,
        ResponseParam,
    ]]


def response_schema(
    success_model: type[ResponseModel] | None,
    *error_codes: int
):
    _map = {
        422: ErrorResponseModel,
        500: ErrorResponseModel,
    }
    return {
        200 if success_model is None else 200: ResponseParam(model=success_model),
    } | {code: ResponseParam(model=_map[code]) for code in error_codes}
