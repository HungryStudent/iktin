from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.utils.callback_data import CallbackData

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton("Создать накладную"),
    KeyboardButton("Создать претензию"),
    KeyboardButton("Вызвать менеджера в чат")
)

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton("Отмена")
)
cancel_dialog = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton("Завершить диалог")
)

files_finish = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton("Завершить"),
    KeyboardButton("Отмена")
)

payment_methods = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("СБП", callback_data="payment_method:sbp"),
    InlineKeyboardButton("Карта", callback_data="payment_method:card")
)
