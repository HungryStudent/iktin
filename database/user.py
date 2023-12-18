from asyncpg import Connection

from database import get_conn


async def add_user(user_id, username, fullname):
    conn: Connection = await get_conn()
    row = await conn.fetchrow(
        "INSERT INTO users(user_id, username, fullname) VALUES ($1, $2, $3) RETURNING *",
        user_id, username, fullname
    )
    await conn.close()
    return row


async def get_users():
    conn: Connection = await get_conn()
    rows = await conn.fetch("SELECT * from users")
    await conn.close()
    return rows


async def get_user(user_id):
    conn: Connection = await get_conn()
    row = await conn.fetchrow("SELECT * from users WHERE user_id = $1", user_id)
    await conn.close()
    return row


async def get_need_chat_users(manager_id):
    conn: Connection = await get_conn()
    rows = await conn.fetch("SELECT * from users WHERE manager_id = $1 and need_chat", manager_id)
    await conn.close()
    return rows


async def set_phone(user_id, phone):
    conn: Connection = await get_conn()
    await conn.execute("UPDATE users SET phone = $1 WHERE user_id = $2", phone, user_id)
    await conn.close()


async def set_poll_answers(user_id, answers):
    conn: Connection = await get_conn()
    await conn.execute("UPDATE users SET first_answer = $1, second_answer = $2, third_answer = $3 WHERE user_id = $4",
                       answers["first"], answers["second"], answers["third"], user_id)
    await conn.close()


async def set_need_chat(user_id, status):
    conn: Connection = await get_conn()
    await conn.execute("UPDATE users SET need_chat = $1 WHERE user_id = $2", status, user_id)
    await conn.close()
