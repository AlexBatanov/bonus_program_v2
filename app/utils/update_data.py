from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import BonusPoint, Buyer
from utils.crud import get_obj


def update_data_user(data: Dict) -> Dict:
    """Обновляем данные для создания юзера"""
    first_name, last_name = data.get('name').split()
    result = dict()
    result['first_name'] = first_name
    result['last_name'] = last_name
    result['telegram_id'] = int(data.get('telegram_id'))
    result['is_admin'] = data.get('is_admin')
    return result

def update_data_cheque(data: Dict) -> Dict:
    """Обновляем данные для создания чека"""
    cheque_data = dict()
    cheque_data['films'] = data.get('films')
    data['amount'] = int(data.get('amount')) - int(data.get('bonus_points'))
    cheque_data['amount'] = data.get('amount')
    cheque_data['employee'] = data.get('employee')
    cheque_data['buyer'] = data.get('buyer')
    return cheque_data

async def update_buyer(async_session: AsyncSession, data: Dict) -> Buyer:
    """Обновляем данные объекта покупатель перед сохраннением изменений"""
    bonus = await get_obj(async_session, BonusPoint, 'name', 'bonus_pointer')
    buyer = await get_obj(async_session, Buyer, 'number', data.get('number'))
    print(data)
    amount = int(data.get('amount'))
    buyer.bonus_points = buyer.bonus_points - int(data.get('bonus_points')) + amount * bonus.percent // 100
    buyer.count_aplications += 1
    return buyer