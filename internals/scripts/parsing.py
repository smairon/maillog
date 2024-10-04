import asyncio

from .. import providers


def logs_parser(rdbs_dsn: str, file_path: str):
    processor = providers.parser.LogsProcessor(rdbs_dsn, file_path)
    asyncio.run(processor())
