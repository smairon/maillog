"""
Очень простая и наивная реализация механизма миграции данных. В реальном проекте, конечно же,
стоит использовать решения типа alembic и нет особого смысла в асинхронном выполнении миграций,
так как эта операция нечастая и без конкурентности.

В данном случае сделана асинхронная реализация
просто чтобы не тащить кучу других зависимостей и переиспользовать библиотеку доступа к БД которая уже используется
"""
import asyncio
import os
import typing

import asyncpg


class Migrator:
    def __init__(self, rdbs_dsn: str, migrations_dir: str):
        self._rdbs_dsn = rdbs_dsn
        self._migrations_dir = migrations_dir

    def upgrade(self):
        asyncio.run(self._upgrade())

    def downgrade(self):
        asyncio.run(self._downgrade())

    async def _upgrade(self):
        await self._process('upgrade')

    async def _downgrade(self):
        await self._process('downgrade')

    async def _process(self, action: typing.Literal['upgrade', 'downgrade']):
        connection = await asyncpg.connect(self._rdbs_dsn)
        try:
            with os.scandir(os.path.join(self._migrations_dir, action)) as entries:
                for entry in sorted(entries, key=lambda e: e.name):
                    if entry.is_file():
                        with open(entry, 'rt') as f:
                            sql = f.read()
                            await connection.execute(sql)
        finally:
            await connection.close()
