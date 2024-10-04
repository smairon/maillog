import typing


class DataQueryProviderContract(typing.Protocol):
    async def get_logs(self, receiver: str) -> tuple[list[dict], int]: ...

