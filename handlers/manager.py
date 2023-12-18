from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import database as db
import keyboards.manager as manager_kb
import keyboards.user as user_kb
from create_bot import dp
from states.manager import ManagerChatStates
from states.user import UserChatStates


@dp.message_handler(text="Претензии от клиентов", state="*")
async def manager_reports(message: Message, state: FSMContext):
    reports = await db.get_reports_by_manager_id(message.from_user.id)
    await message.answer("Претензии:", reply_markup=manager_kb.get_reports(reports))


@dp.message_handler(text="Чаты с клиентами")
async def need_chat_users_request(message: Message, state: FSMContext):
    need_chat_users = await db.get_need_chat_users(message.from_user.id)
    await message.answer("Клиенты, вызвавшие в чат:", reply_markup=manager_kb.get_need_chat_users(need_chat_users))


@dp.callback_query_handler(Text(startswith="manager_report"))
async def manager_report(call: CallbackQuery, state: FSMContext):
    report_id = int(call.data.split(":")[1])
    report = await db.get_report(report_id)
    await call.message.answer(f"""
@{report["username"]}
{report["invoice_id"]}
{report["email"]}
{report["description"]}
{report["amount"]}
""")


@dp.callback_query_handler(Text(startswith="connect_to_chat"))
async def connect_to_chat(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.split(":")[1])
    await call.bot.send_message(user_id, "Менеджер подключен, можно вести диалог", reply_markup=user_kb.cancel_dialog)
    user_state = dp.current_state(chat=user_id, user=user_id)
    await user_state.set_state(UserChatStates.text)
    await user_state.update_data(manager_id=call.from_user.id)

    await state.set_state(ManagerChatStates.text)
    await state.update_data(user_id=user_id)
    await call.message.edit_text("Вы подключены к чату, можно вести диалог")

    await db.set_need_chat(user_id, False)


@dp.message_handler(state=ManagerChatStates.text)
async def chat_text(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    await message.bot.send_message(user_id, message.text)
