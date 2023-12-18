from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateInvoiceStates(StatesGroup):
    description = State()
    weight = State()
    size = State()
    sending_address = State()
    receiving_address = State()
    payment_method = State()


class CreateReportStates(StatesGroup):
    invoice_id = State()
    email = State()
    description = State()
    amount = State()
    files = State()

class UserChatStates(StatesGroup):
    text = State()
