from asyncpg import Connection

from database import get_conn


async def add_invoice(user_id, description, weight, size, sending_address, receiving_address, payment_method):
    conn: Connection = await get_conn()
    row = await conn.fetchrow(
        "INSERT INTO invoice(user_id, description, weight, size, sending_address, receiving_address, payment_method)"
        " VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *",
        user_id, description, weight, size, sending_address, receiving_address, payment_method
    )
    await conn.close()
    return row
