from asyncpg import Connection

from database import get_conn


async def add_report(user_id, invoice_id, email, description, amount, files):
    conn: Connection = await get_conn()
    row = await conn.fetchrow(
        "INSERT INTO report(user_id, invoice_id, email, description, amount)"
        " VALUES ($1, $2, $3, $4, $5) RETURNING *",
        user_id, invoice_id, email, description, amount
    )
    for file in files:
        await conn.execute("INSERT INTO report_files VALUES ($1, $2, $3)",
                           row["report_id"], file["file_id"], file["file_type"])
    await conn.close()
    return row


async def get_report(report_id):
    conn: Connection = await get_conn()
    row = await conn.fetchrow("SELECT * FROM report join users u on report.user_id = u.user_id where report_id = $1",
                              report_id)
    await conn.close()
    return row

async def get_reports_by_manager_id(manager_id):
    conn: Connection = await get_conn()
    rows = await conn.fetch("select * from report join users u on report.user_id = u.user_id where manager_id = $1",
                            manager_id)
    await conn.close()
    return rows
