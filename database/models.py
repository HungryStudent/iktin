from asyncpg import Connection

from database import get_conn


async def create_models():
    conn: Connection = await get_conn()
    await conn.execute("CREATE TABLE IF NOT EXISTS users("
                       "user_id BIGINT PRIMARY KEY,"
                       "username VARCHAR,"
                       "fullname VARCHAR,"
                       "reg_time TIMESTAMP DEFAULT NOW(),"
                       "manager_id BIGINT,"
                       "is_manager BOOLEAN DEFAULT FALSE,"
                       "need_chat BOOLEAN DEFAULT FALSE"
                       ")")
    await conn.execute("CREATE TABLE IF NOT EXISTS invoice("
                       "invoice_id SERIAL,"
                       "user_id BIGINT,"
                       "description VARCHAR,"
                       "weight INTEGER,"
                       "size VARCHAR,"
                       "sending_address VARCHAR,"
                       "receiving_address VARCHAR,"
                       "payment_method VARCHAR"
                       ")")
    await conn.execute("CREATE TABLE IF NOT EXISTS report("
                       "report_id SERIAL,"
                       "user_id BIGINT,"
                       "invoice_id INTEGER,"
                       "email VARCHAR,"
                       "description VARCHAR,"
                       "amount INTEGER"
                       ")")
    await conn.execute("CREATE TABLE IF NOT EXISTS report_files("
                       "report_id INTEGER,"
                       "file_id VARCHAR,"
                       "file_type VARCHAR"
                       ")")

    await conn.close()
