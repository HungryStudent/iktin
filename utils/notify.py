from datetime import timedelta, datetime

from apscheduler.jobstores.base import ConflictingIdError

import database as db
from create_bot import scheduler, bot


async def notify(user_id, msg):
    user = await db.get_user(user_id)

    await bot.send_message(user["manager_id"], f"""
Пользователь: @{user["username"]}
{msg}""")


def create_notify(user_id, msg):
    run_date = datetime.now() + timedelta(seconds=5)
    try:
        scheduler.add_job(notify, "date", run_date=run_date, args=(user_id, msg), id=str(user_id))
    except ConflictingIdError:
        scheduler.remove_job(str(user_id))
        scheduler.add_job(notify, "date", run_date=run_date, args=(user_id, msg), id=str(user_id))


def remove_notify(user_id):
    scheduler.remove_job(str(user_id))
