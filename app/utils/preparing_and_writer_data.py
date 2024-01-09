import asyncio
from typing import List

import openpyxl

from db.models import Buyer, Employee
from utils.crud import get_all_obj
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


def write_in_file(data: List[List[str]]) -> None:
    """Записываем данные в файл"""
    wb = openpyxl.Workbook()
    wb.create_sheet(title = 'Отчет', index = 0)
    sheet = wb['Отчет']
    for row in range(1, len(data) + 1):
        for col in range(1, len(data[0]) + 1):
            value = data[row-1][col-1]
            cell = sheet.cell(row = row, column = col)
            cell.value = value
    print('end')
    wb.save('example.xlsx')


async def send_data(callback, data):
    coro = asyncio.to_thread(write_in_file, data)
    task = asyncio.create_task(coro)
    await asyncio.sleep(0)
    await task

    doc = FSInputFile(r'./example.xlsx', 'otchet.xlsx')
    await callback.message.answer_document(doc)
    await callback.answer()