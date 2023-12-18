import logging

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_parser import TOKEN

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger("logs")

stor = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=stor)
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = AsyncIOScheduler(jobstores=jobstores)
