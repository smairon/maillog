import collections.abc

import fastapi
import specs


class Application(fastapi.FastAPI):
    query_provider: specs.providers.DataQueryProviderContract
    logs_processor: collections.abc.Callable


class Request(fastapi.Request):
    app: Application
