
from typing import Dict
from db.models import Buyer
from utils.crud import get_obj


def update_data_user(data: Dict) -> Dict:
    """Обновляем данные для создания юзера"""
    first_name, last_name = data.get('name').split()
    data['first_name'] = first_name
    data['last_name'] = last_name
    data['telegram_id'] = int(data.get('telegram_id'))
    del data['name']
    return data


def update_data_cheque(data: Dict) -> Dict:
    """Обновляем данные для создания чека"""
    cheque_data = dict()
    cheque_data['films'] = data.get('films')
    data['amount'] = int(data.get('amount')) - int(data.get('bonus_points'))
    cheque_data['amount'] = data.get('amount')
    cheque_data['employee'] = data.get('employee')
    cheque_data['buyer'] = data.get('buyer')
    return cheque_data