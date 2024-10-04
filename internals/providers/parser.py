import datetime
import typing
import collections.abc

import asyncpg
import re


class LogItem(typing.TypedDict):
    dt: datetime.datetime
    id: str
    int_id: str
    flag: str | None
    address: str | None
    log_string: str


"""
Инкапсуляция логики разбора лога. 
Таких классов можно делать сколько угодно. 
В данном случае несколько нарушается любимый многими принцип единой ответственности (логика чтения данных и их разбора)
В реальном проекте стоит их разнести по разным уровням. 
Это, в том числе, поможет отделить CPU-bound задачу по разбору лога от IO-bound задачи по чтению данных с диска.
"""


class MailLog:
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, filepath: str):
        self._filepath = filepath
        self._flags = ('<=', '=>', '->', '**', '==')

    def __iter__(self) -> collections.abc.Generator[None, None, tuple[str, LogItem]]:
        with open(self._filepath, 'rt') as f:
            for line in f.readlines():
                item = self._parse_line(line)
                yield self._define_table(item), item

    @staticmethod
    def _define_table(item: LogItem):
        if item.get("flag") == '<=':
            return 'message'
        else:
            return 'log'

    def _parse_line(self, line: str) -> LogItem:
        row = line.split()
        return dict(
            dt=datetime.datetime.strptime(" ".join(row[:2]), self.DATE_FORMAT),
            id=re.search(r'id=([^ ]+)', line).group(1),
            int_id=row[2],
            flag=row[3] if row[3] in self._flags else None,
            address=row[4] if row[3] in self._flags else None,
            log_string=" ".join(row[2:])
        )


"""
Так как в задании формат лога один, то нет смысла заморачиваться с поддержкой разных форматов. 
В реальном проекте есть смысл конкретную реализацию разбора лога передавать параметром
"""


class LogsProcessor:
    def __init__(self, rdbs_dsn: str, file_path: str):
        self._rdbs_dsn = rdbs_dsn
        self._log = MailLog(file_path)

    async def __call__(self):
        data = collections.defaultdict(list)
        """
        Здесь имеем тяжелую синхронную операцию по разбору лога, поэтому в реальном проекте стоит 
        ее вынести в отдельный process_pool.
         Но вообще, стоит подумать вообще над целесообразностью применения 
         асинхронного подхода в задаче импорта логов в БД. 
         В большинстве случаев подойдет синхронный подход.
        """
        for table, item in self._log:
            data[table].append(
                getattr(self, f'_format_{table}_row')(item)
            )
        await self._store(data)

    @staticmethod
    def _format_message_row(item: LogItem):
        return (
            item['dt'],
            item['id'],
            item['int_id'],
            item['log_string'],
            None
        )

    @staticmethod
    def _format_log_row(item: LogItem):
        return (
            item['dt'],
            item['int_id'],
            item['log_string'],
            item['address'],
        )

    async def _store(self, data: dict[str, list[tuple]]):
        connection = await asyncpg.connect(self._rdbs_dsn)
        try:
            for table, rows in data.items():
                await connection.copy_records_to_table(table, records=rows)
        finally:
            await connection.close()
