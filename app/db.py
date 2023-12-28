from contextlib import asynccontextmanager

import asyncpg

from app.config import POSTGRES_DB, POSTGRES_PORT, POSTGRES_PASSWORD, \
    POSTGRES_USER, POSTGRES_HOST


async def get_conn():
    conn: asyncpg.Connection = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        port=POSTGRES_PORT)

    return conn


@asynccontextmanager
async def get_connection():
    conn = await get_conn()
    try:
        yield conn
    finally:
        await conn.close()


def with_connection(func):
    async def wrapper(*args, **kwargs):
        async with get_connection() as conn:
            return await func(conn=conn, *args, **kwargs)

    return wrapper
