from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import database as db
import keyboards.manager as manager_kb
import keyboards.user as user_kb
from create_bot import dp
from states.user import UserChatStates


@dp.message_handler(text="Вызвать менеджера в чат", state="*")
async def start_chat(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Уведомление отправлено менеджеру, ожидайте", reply_markup=user_kb.menu)
    await db.set_need_chat(message.from_user.id, True)
    user = await db.get_user(message.from_user.id)
    manager_id = user["manager_id"]
    await message.bot.send_message(manager_id, f"@{user['username']} вызывает вас в чат",
                                   reply_markup=manager_kb.connect_to_chat(message.from_user.id))


@dp.message_handler(state=UserChatStates.text)
async def chat_text(message: Message, state: FSMContext):
    data = await state.get_data()
    manager_id = data["manager_id"]
    if message.text == "Завершить диалог":
        await state.finish()
        manager_state = dp.current_state(chat=manager_id, user=manager_id)
        await manager_state.finish()

        await message.answer("Диалог закончен", reply_markup=user_kb.menu)
        await message.bot.send_message(manager_id, "Диалог закончен", reply_markup=manager_kb.menu)
    await message.bot.send_message(manager_id, message.text)
