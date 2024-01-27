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

    """CREATE TABLE IF NOT EXISTS customers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
email VARCHAR(50) NOT NULL,
messenger_id INTEGER NOT NULL,

UNIQUE (email, messenger_id),
FOREIGN KEY (messenger_id) REFERENCES messengers(id)
);""",
    """CREATE TABLE IF NOT EXISTS tickets_customers (
ticket_id VARCHAR(200) NOT NULL,
customer_id INTEGER NOT NULL,

PRIMARY KEY (ticket_id, customer_id),
FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE,
FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);""",

    """CREATE TABLE IF NOT EXISTS operators_messages(
id VARCHAR(200) PRIMARY KEY);""",
    """INSERT INTO messengers (name) VALUES
('vkontakte'),
('telegram'),
('vk_wall');"""
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
                          ticket_id: str | None):
    result = await conn.execute_insert(
        'INSERT INTO customers (email, messenger_id)'
        'VALUES (?, ?)',
        (email, messenger_id)
    )

    if ticket_id:
        await conn.execute(
            'INSERT INTO tickets (id) VALUES (?);',
            (ticket_id,)
        )

        await conn.execute(
            'INSERT INTO tickets_customers (ticket_id, customer_id)'
            'VALUES (?, ?)',
            (ticket_id, result[0])
        )
    await conn.commit()
    return result[0]


@with_connection
async def get_customer_ticket_id(conn: Connection,
                                 email: str,
                                 messenger_id: int):
    result: list[tuple] = await conn.execute_fetchall(
        'SELECT tc.ticket_id FROM customers c JOIN tickets_customers tc ON '
        'c.id = tc.customer_id WHERE c.email = ? AND c.messenger_id = ?',
        (email, messenger_id)
    )
    return result[0][0] if result else result


@with_connection
async def update_customer_ticket_id(conn: Connection,
                                    email: str,
                                    messenger_id: int,
                                    ticket_id: str | None):
    if not ticket_id:
        return

    await conn.execute(
        'INSERT INTO tickets (id) VALUES (?);',
        (ticket_id,)
    )

    await conn.execute(
        'INSERT INTO tickets_customers (ticket_id, customer_id) '
        'VALUES (?, (SELECT id FROM customers WHERE email = ? AND '
        'messenger_id = ?))',
        (ticket_id, email, messenger_id)
    )

    await conn.commit()


@with_connection
async def unset_customer_ticket_id(
        conn: Connection,
        ticket_id: str,
):
    await conn.execute(
        'DELETE FROM tickets WHERE id = ?',
        (ticket_id,)
    )
    await conn.commit()


@with_connection
async def get_customer_by_ticket_id(
        conn: Connection,
        ticket_id: str
) -> tuple:
    result: list = await conn.execute_fetchall(
        'SELECT c.email, c.messenger_id FROM customers c JOIN '
        'tickets_customers tc ON c.id = tc.customer_id WHERE '
        'tc.ticket_id = ?',
        (ticket_id,)
    )
    return result[0] if result else None


@with_connection
async def create_vk_comment(
        conn: Connection,
        comment_id: int,
        post_id: int,
        group_id: int,
        customer_id: int,
        ticket_id: str | None,
):
    await conn.execute(
        'INSERT INTO tickets (id) VALUES (?);',
        (ticket_id,)
    )

    await conn.execute(
        'INSERT INTO vk_comments (id, post_id, group_id, ticket_id, '
        'customer_id) VALUES (?, ?, ?, ?, ?)',
        (comment_id, post_id, group_id, ticket_id, customer_id)
    )
    await conn.commit()


@with_connection
async def get_comment_by_ticket_id(conn: Connection, ticket_id: str) -> tuple:
    result: list = await conn.execute_fetchall(
        'SELECT * FROM vk_comments WHERE ticket_id = ?',
        (ticket_id,)
    )
    return result[0]


@with_connection
async def insert_operator_answer(conn: Connection, answer_id: str):
    await conn.execute(
        'INSERT INTO operators_messages (id) VALUES (?)',
        (answer_id,)
    )

    await conn.commit()


@with_connection
async def get_operator_answer_by_id(conn: Connection, answer_id: str):
    result: list = await conn.execute_fetchall(
        'SELECT id FROM operators_messages WHERE id = ?',
        (answer_id,)
    )
    return result[0] if result else None


@with_connection
async def check_customer_in_db(conn: Connection, email: str,
                               messenger_id: int):
    result: list = await conn.execute_fetchall(
        'SELECT email, messenger_id FROM customers WHERE email = ? AND '
        'messenger_id = ?',
        (email, messenger_id)
    )
    return result[0] if result else None


@with_connection
async def get_customer_id(conn: Connection, email: str,
                          messenger_id: int):
    result: list = await conn.execute_fetchall(
        'SELECT id FROM customers WHERE email = ? AND '
        'messenger_id = ?',
        (email, messenger_id)
    )
    return result[0][0] if result else None
