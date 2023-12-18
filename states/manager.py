from aiogram.dispatcher.filters.state import StatesGroup, State


class ManagerChatStates(StatesGroup):
    text = State()
