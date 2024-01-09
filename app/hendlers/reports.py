import asyncio
from typing import List

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from utils.preparing_and_writer_data import (
    get_data_all_buyers, get_data_all_employee, send_data
)
from keyboards import kb
from middlewares.user_acces import CheckAdmin


reports_router = Router()
reports_router.message.middleware(CheckAdmin())


@reports_router.message(F.text.lower() == 'отчеты')
async def report_choice(message: Message, state: FSMContext):
    """Выводим кнопки с выбором отчета"""
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
    """Отправляем файл xlsx со всеми сотрудниками"""
    data = await get_data_all_buyers()
    await send_data(callback, data)

