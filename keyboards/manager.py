from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.utils.callback_data import CallbackData

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton("Чаты с клиентами"),
    KeyboardButton("Претензии от клиентов")
)


def get_reports(reports):
    kb = InlineKeyboardMarkup(row_width=1)
    for report in reports:
        kb.add(
            InlineKeyboardButton(f"{report['invoice_id']} - @{report['username']}",
                                 callback_data=f"manager_report:{report['report_id']}")
        )
    return kb


def get_need_chat_users(need_chat_users):
    kb = InlineKeyboardMarkup(row_width=1)
    for user in need_chat_users:
        kb.add(InlineKeyboardButton("@" + user["username"], callback_data=f"connect_to_chat:{user['user_id']}"))
    return kb


def connect_to_chat(user_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Подключиться", callback_data=f"connect_to_chat:{user_id}"))
    return kb
