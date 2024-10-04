import asyncpg


class DataQueryProvider:
    def __init__(self, rdbs_dsn: str):
        self._pool = None
        self._rdbs_dsn = rdbs_dsn

    async def get_logs(self, receiver: str) -> tuple[list[dict], int]:
        pool = await self._get_pool()
        async with pool.acquire() as connection:
            """
            Организация схемы данных не совсем оптимальна, стоит подумать над более удачной реализацией
            """
            rows = await connection.fetch(
                """
                SELECT 
                    created, str, int_id 
                FROM log 
                WHERE address = $1
                UNION
                SELECT 
                    created, str, int_id 
                FROM message 
                WHERE int_id in (SELECT int_id FROM log WHERE address = $1)
                ORDER BY int_id, created
                """,
                receiver
            )
            return [
                {'timestamp': row['created'], 'message': row['str']} for row in rows[:100]
            ], len(rows)

    async def _get_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._rdbs_dsn)
        return self._pool
