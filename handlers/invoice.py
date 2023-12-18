from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import database as db
import keyboards.user as user_kb
from create_bot import dp
from states.user import CreateInvoiceStates
from utils import notify as notify_utils
from utils import pdf as pdf_utils


@dp.message_handler(text="Создать накладную", state="*")
async def create_invoice(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Введите описание груза", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь начал создание накладной")
    await state.set_state(CreateInvoiceStates.description)


@dp.message_handler(state=CreateInvoiceStates.description)
async def create_invoice_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите вес груза", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь ввел описание груза")
    await state.set_state(CreateInvoiceStates.weight)


@dp.message_handler(state=CreateInvoiceStates.weight)
async def create_invoice_weight(message: Message, state: FSMContext):
    try:
        await state.update_data(weight=int(message.text))
    except ValueError:
        await message.answer("Введите целое число", reply_markup=user_kb.cancel)
        notify_utils.create_notify(message.from_user.id, "Пользователь ввел описание груза")
    await message.answer("Введите габариты груза", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь ввел описание, вес груза")
    await state.set_state(CreateInvoiceStates.size)


@dp.message_handler(state=CreateInvoiceStates.size)
async def create_invoice_size(message: Message, state: FSMContext):
    await state.update_data(size=message.text)
    await message.answer("Введите точный адрес отправки", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь ввел описание, вес, габариты груза")
    await state.set_state(CreateInvoiceStates.sending_address)


@dp.message_handler(state=CreateInvoiceStates.sending_address)
async def create_invoice_sending_address(message: Message, state: FSMContext):
    await state.update_data(sending_address=message.text)
    await message.answer("Введите точный адрес получения", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь ввел описание, вес, габариты, адрес отправки груза")
    await state.set_state(CreateInvoiceStates.receiving_address)


@dp.message_handler(state=CreateInvoiceStates.receiving_address)
async def create_invoice_receiving_address(message: Message, state: FSMContext):
    await state.update_data(receiving_address=message.text)
    await message.answer("Выберите способ оплаты", reply_markup=user_kb.payment_methods)
    notify_utils.create_notify(message.from_user.id,
                               "Пользователь ввел описание, вес, габариты, адрес отправки, адрес получения груза")
    await state.set_state(CreateInvoiceStates.payment_method)


@dp.callback_query_handler(Text(startswith="payment_method"), state=CreateInvoiceStates.payment_method)
async def create_invoice_payment_method(call: CallbackQuery, state: FSMContext):
    await state.update_data(payment_method=call.data.split(":")[1])
    data = await state.get_data()
    notify_utils.remove_notify(call.from_user.id)
    invoice = await db.add_invoice(call.from_user.id, **data)
    data["invoice_id"] = invoice["invoice_id"]
    pdf_utils.gen_doc(data)
    await call.message.answer_document(open(f'{invoice["invoice_id"]}.pdf', "rb"), caption="Накладная успешно создана")
    await call.answer()
