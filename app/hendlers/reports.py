from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.update_data import parse_date_string
from utils.states import DateForm
from utils.validators import chek_correct_data
from utils.preparing_and_writer_data import (
    get_cheques_by_date, get_data_all_buyers, get_data_all_cheques,
    get_data_all_employee, get_data_today_cheques, send_data
)
from keyboards import kb
from middlewares.user_acces import CheckAdmin


reports_router = Router()
reports_router.message.middleware(CheckAdmin())


@reports_router.message(F.text.lower() == 'отчеты')
async def report_choice(message: Message, state: FSMContext):
    """Выводим кнопки с выбором отчета"""
    await state.clear()
    await message.answer(
        'Статистика будет отправлена в виде exel документа',
        reply_markup=kb.list_reports()
        )


@reports_router.callback_query(F.data == 'list_employees')
async def send_employees_data_file(callback: CallbackQuery, state: FSMContext):
    """Отправляем файл xlsx со всеми сотрудниками"""
    data = await get_data_all_employee()
    await send_data(callback, data)


@reports_router.callback_query(F.data == 'list_buyers')
async def send_buyers_data_file(callback: CallbackQuery, state: FSMContext):
    """Отправляем файл xlsx со всеми покупателями"""
    data = await get_data_all_buyers()
    await send_data(callback, data)


@reports_router.callback_query(F.data == 'info_cheques')
async def report_choise_cheques(callback: CallbackQuery, state: FSMContext):
    """Варианты отчета для чеков"""
    await callback.message.answer(
        'Варианты отчета', reply_markup=kb.report_cheques()
    )
    await callback.answer()


@reports_router.callback_query(F.data == 'all_cheques')
async def send_cheques_data_file(callback: CallbackQuery, state: FSMContext):
    """Отправляем файл xlsx со всеми чеками"""
    data = await get_data_all_cheques()
    await send_data(callback, data)


@reports_router.callback_query(F.data == 'cheques_today')
async def send_today_cheques_data_file(callback: CallbackQuery, state: FSMContext):
    """Отправляем файл xlsx с чеками за текущий день"""
    data = await get_data_today_cheques()
    await send_data(callback, data)


@reports_router.callback_query(F.data == 'cheques_for')
async def requesting_data(callback: CallbackQuery, state: FSMContext):
    """Запрашиваем дату для отчета, с какого по какое число"""
    await callback.message.answer(
        'Введи дату с какого по какое, данные будут включительны\n'
        'Пример: 10.01.2024 - 16.02.2024'
    )
    await state.set_state(DateForm.date)
    await callback.answer()


@reports_router.message(DateForm.date)
async def requesting_data(message: Message, state: FSMContext):
    """Отправляем xlsx файл с чеками за указанный период"""
    err_msg = chek_correct_data(message.text)
    if err_msg:
        await message.answer(err_msg)
        return
    dates = message.text.split()
    start, end = parse_date_string(dates[0]), parse_date_string(dates[-1])
    data = await get_cheques_by_date(start, end)
    await send_data(message, data)
    await state.clear()


