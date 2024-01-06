from typing import Dict
from utils.crud import get_obj
from db.async_engine import async_session
from db.models import Buyer, Employee


async def is_valid_data_user(data: Dict) -> str | None:
    if len(data.get('name').split()) != 2:
        return 'Имя и фамилия должны быть написаны через пробел'
    if not data.get('telegram_id').isdigit():
        return 'Telegram ID должен содержать только числа'
    user = await get_obj(async_session, Employee, 'telegram_id', int(data.get('telegram_id')))
    if user:
        return 'Сотрудник с таким Telegram ID уже зарегистрирован'


async def is_valid_data_cheque_buyer(data: Dict) -> str | None:
    if not data.get('amount').isdigit():
        return 'В сумме покупки должны быть только числа'
    bonus = data.get('bonus_points')
    if not bonus.isdigit():
        return 'В бонусах должны быть только числа'
    buyer = await get_obj(async_session, Buyer, 'number', data.get('number'))
    if int(bonus) > int(data.get('amount')):
        return 'Введеные бонусы не могут быть больше суммы чека'
    if int(bonus) > buyer.bonus_points:
        return 'Введеные бонусы привышают баллы клиента'


def is_valid_tg_id(id: str) -> str | bool:
    if not id.isdigit():
        return 'Telegram ID должен содержать только числа'