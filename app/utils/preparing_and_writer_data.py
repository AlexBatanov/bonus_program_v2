import asyncio
from typing import List

import openpyxl
from aiogram.types import Message, CallbackQuery

from db.models import Buyer, Cheque, Employee
from utils.crud import get_all_obj, get_obj_by_id, get_objects_by_date, get_objects_today
from db.async_engine import async_session
from aiogram.types.input_file import FSInputFile


async def get_data_all_employee():
    """Получаем всех сотрудников и формируем в лист для дальнейшей записи в файл"""
    employees = await get_all_obj(async_session, Employee)
    result = [['Телеграм_id', 'Фамилия Имя', 'Количество чеков', 'Общая сумма'],]
    for employee in employees:
        cur_data = [
            employee.telegram_id,
            f'{employee.last_name} {employee.first_name}',
            len(employee.cheques),
            sum(cheque.amount for cheque in employee.cheques),
        ]
        result.append(cur_data)
    return result


async def get_data_all_buyers():
    """Получаем всех покупателей и формируем в лист для дальнейшей записи в файл"""
    buyers = await get_all_obj(async_session, Buyer)
    result = [['Номер телефона', 'Имя', 'Количество чеков', 'Общая сумма покупок'],]
    for buyer in buyers:
        cur_data = [
            buyer.number,
            buyer.name,
            buyer.count_aplications,
            sum(cheque.amount for cheque in buyer.cheques),
        ]
        result.append(cur_data)
    return result


async def get_data_all_cheques():
    """Получаем всех покупателей и формируем в лист для дальнейшей записи в файл"""
    cheques = await get_all_obj(async_session, Cheque)
    return await get_list_cheques(cheques)


async def get_data_today_cheques():
    """Получаем всех покупателей и формируем в лист для дальнейшей записи в файл"""
    cheques = await get_objects_today(async_session, Cheque, 'date')
    return await get_list_cheques(cheques)
    

async def get_cheques_by_date(start, end):
    """
    Получаем всех покупателей за предоставленый период
    формируем в лист для дальнейшей записи в файл
    """
    cheques = await get_objects_by_date(async_session, Cheque, 'date', start, end)
    return await get_list_cheques(cheques)


async def get_list_cheques(cheques):
    """подготавливаем данные для записи в таблицу"""
    sum_amount = sum(cheque.amount for cheque in cheques)
    result = [
        ['Общая сумма', sum_amount, '-', '-', '-'],
        ['Установленные пленки', 'Сумма', 'Дата', 'Имя клиента', 'Номер телефона'],
    ]
    for cheque in cheques:
        buyer = await get_obj_by_id(async_session, Buyer, cheque.buyer)
        cur_data = [
            cheque.films,
            cheque.amount,
            cheque.date,
            buyer.name,
            buyer.number
        ]
        result.append(cur_data)
    return result


def write_in_file(data: List[List[str]]) -> None:
    """Записываем данные в файл"""
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    for row in range(1, len(data) + 1):
        for col in range(1, len(data[0]) + 1):
            value = data[row-1][col-1]
            cell = sheet.cell(row = row, column = col)
            cell.value = value
    wb.save('example.xlsx')


async def send_data(callback: Message | CallbackQuery, data):
    """создаем поток для блокирующей функции, по завершению отправляем файл"""
    coro = asyncio.to_thread(write_in_file, data)
    task = asyncio.create_task(coro)
    await asyncio.sleep(0)
    await task

    doc = FSInputFile(r'./example.xlsx', 'otchet.xlsx')
    if isinstance(callback, CallbackQuery):
        await callback.message.answer_document(doc)
        await callback.answer()
    else:
        await callback.answer_document(doc)