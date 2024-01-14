from contextlib import asynccontextmanager
from sqlite3 import IntegrityError

from aiosqlite import Connection, connect

from app.config import DB_PATH

queries = [
    """CREATE TABLE IF NOT EXISTS tickets(
id VARCHAR(200) PRIMARY KEY
);""",

    """CREATE TABLE IF NOT EXISTS messengers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(50) UNIQUE NOT NULL
);""",

    """
CREATE TABLE IF NOT EXISTS customers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
email VARCHAR(50) NOT NULL,
messenger_id INTEGER NOT NULL,
ticket_id VARCHAR(200),

UNIQUE (email, messenger_id),
FOREIGN KEY (messenger_id) REFERENCES messengers(id),
FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE SET NULL
);""",

    """INSERT INTO messengers (name) VALUES
('vkontakte'),
('telegram');"""
]


async def get_conn() -> Connection:
    conn: Connection = await connect(DB_PATH)
    return conn


@asynccontextmanager
async def get_connection():
    conn: Connection = await get_conn()
    try:
        yield conn
    finally:
        await conn.close()


def with_connection(func):
    async def wrapper(*args, **kwargs):
        async with get_connection() as conn:
            await conn.execute("PRAGMA foreign_keys = ON;")
            return await func(conn=conn, *args, **kwargs)

    return wrapper


@with_connection
async def db_on_start(conn: Connection):
    try:
        for query in queries:
            await conn.execute(query)
            await conn.commit()
    except IntegrityError:
        pass


@with_connection
async def create_customer(conn: Connection,
                          email: str,
                          messenger_id: int,
                          ticket_id: str):
    await conn.execute(
        'INSERT INTO tickets (id) VALUES (?);',
        (ticket_id,)
    )

    await conn.execute(
        'INSERT INTO customers (email, messenger_id, ticket_id)'
        'VALUES (?, ?, ?)',
        (email, messenger_id, ticket_id)
    )
    await conn.commit()


@with_connection
async def get_customer_ticket_id(conn: Connection,
                                 email: str):
    result: list[tuple] = await conn.execute_fetchall(
        'SELECT ticket_id FROM customers WHERE email = ?',
        (email,)
    )
    return result[0][0] if result else result


@with_connection
async def update_customer_ticket_id(conn: Connection,
                                    email: str,
                                    ticket_id: str):
    await conn.execute(
        'INSERT INTO tickets (id) VALUES (?);',
        (ticket_id,)
    )

    await conn.execute(
        'UPDATE customers SET ticket_id = ? WHERE email = ?',
        (ticket_id, email)
    )

    await conn.commit()


@with_connection
async def unset_customer_ticket_id(
        conn: Connection,
        ticket_id: str,
):
    #ticket_result: list[tuple] = await conn.execute_fetchall(
    #    "SELECT ticket_id FROM customers WHERE email = ?",
    #    (email,)
    #)
    #ticket_id: str = ticket_result[0][0]
    await conn.execute(
        'DELETE FROM tickets WHERE id = ?',
        (ticket_id,)
    )
    await conn.commit()
@with_connection
async def get_customers_by_ticket_id(
        conn:Connection,
        ticket_id: str
) -> list[tuple]:
    return await conn.execute_fetchall(
        'SELECT email, messenger_id FROM customers WHERE ticket_id = ?',
        (ticket_id,)
    )

