from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import database as db
import keyboards.user as user_kb
from create_bot import dp
from states.user import CreateReportStates
from utils import notify as notify_utils


@dp.message_handler(text="Создать претензию", state="*")
async def create_report(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Введите номер накладной", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь начал создание претензии")

    await state.set_state(CreateReportStates.invoice_id)


@dp.message_handler(state=CreateReportStates.invoice_id)
async def create_report_invoice_id(message: Message, state: FSMContext):
    try:
        invoice_id = int(message.text)
    except ValueError:
        return await message.answer("Введите целое число!")
    await state.update_data(invoice_id=invoice_id)
    await message.answer("Введите email для ответа на претензию", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь ввёл номер накладной")
    await state.set_state(CreateReportStates.email)


@dp.message_handler(state=CreateReportStates.email)
async def create_report_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите описание ситуации", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь ввёл номер накладной, email")
    await state.set_state(CreateReportStates.description)


@dp.message_handler(state=CreateReportStates.description)
async def create_report_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите требуемую сумму", reply_markup=user_kb.cancel)
    notify_utils.create_notify(message.from_user.id, "Пользователь ввёл номер накладной, email, описание")
    await state.set_state(CreateReportStates.amount)


@dp.message_handler(state=CreateReportStates.amount)
async def create_report_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        return await message.answer("Введите целое число!")
    await state.update_data(amount=amount)
    await message.answer("Пришлите фото/сканы, когда закончите, нажмите на кнопку 'Завершить'",
                         reply_markup=user_kb.files_finish)
    notify_utils.create_notify(message.from_user.id, "Пользователь ввёл номер накладной, email, требуемую сумму")
    await state.update_data(files=[])
    await state.set_state(CreateReportStates.files)


@dp.message_handler(state=CreateReportStates.files, text="Завершить")
async def create_report_files_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    await notify_utils.remove_notify(message.from_user.id)
    report = await db.add_report(message.from_user.id, **data)
    await message.answer("Претензия составлена и отправлена на рассмотрение", reply_markup=user_kb.menu)
    await state.finish()

    user = await db.get_user(message.from_user.id)
    await message.bot.send_message(user["manager_id"], text=f"""
Новая претензия: @{message.from_user.username}
{report["invoice_id"]}
{report["email"]}
{report["description"]}
{report["amount"]}
""")


@dp.message_handler(state=CreateReportStates.files, content_types="photo")
async def create_report_files_photo(message: Message, state: FSMContext):
    photo_data = {"file_id": message.photo[-1].file_id, "file_type": "photo"}
    data = await state.get_data()
    files = data["files"]
    files.append(photo_data)
    await state.update_data(files=files)
    await message.answer("Вы прислали фото", reply_markup=user_kb.files_finish)


@dp.message_handler(state=CreateReportStates.files, content_types="document")
async def create_report_files_document(message: Message, state: FSMContext):
    document_data = {"file_id": message.document.file_id, "file_type": "document"}
    data = await state.get_data()
    files = data["files"]
    files.append(document_data)
    await state.update_data(files=files)
    await message.answer("Вы прислали документ", reply_markup=user_kb.files_finish)
