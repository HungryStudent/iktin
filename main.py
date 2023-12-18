from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram.utils import executor
from aiogram.utils.exceptions import ChatNotFound

from config_parser import ADMINS
from create_bot import dp, bot, scheduler
import database as db
import handlers


async def on_startup(_):
    await db.create_models()


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
