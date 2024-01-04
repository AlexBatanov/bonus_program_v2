from utils.crud import get_obj
from db.async_engine import async_session
from db.models import Employee


async def is_valid_data_user(data):
    if len(data.get('name').split()) != 2:
        return 'Имя и фамилия должны быть написаны через пробел'
    if not data.get('telegram_id').isdigit():
        return 'Telegram ID должен содержать только числа'
    user = await get_obj(async_session, Employee, 'telegram_id', int(data.get('telegram_id')))
    if user:
        return 'Сотрудник с таким Telegram ID уже зарегистрирован'