from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import database as db
import keyboards.manager as manager_kb
import keyboards.user as user_kb
from create_bot import dp


@dp.message_handler(commands=['start'], state="*")
async def start_command(message: Message, state: FSMContext):
    await state.finish()
    user = await db.get_user(message.from_user.id)

    if user is None:
        user = await db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)

    if user["is_manager"]:
        msg = "Привет, менеджер"
        kb = manager_kb.menu
    else:
        msg = "Привет, клиент"
        kb = user_kb.menu
    await message.answer(msg, reply_markup=kb)


@dp.message_handler(text="Отмена", state="*")
async def cancel_handler(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Ввод отменён")
    user = await db.get_user(message.from_user.id)

    if user["is_manager"]:
        msg = "Привет, менеджер"
        kb = manager_kb.menu
    else:
        msg = "Привет, клиент"
        kb = user_kb.menu
    await message.answer(msg, reply_markup=kb)
