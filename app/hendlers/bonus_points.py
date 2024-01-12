from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from middlewares.user_acces import CheckAdmin
from db.models import BonusPoint
from db.async_engine import async_session
from utils.crud import get_obj, update_obj
from utils.states import BonusForm


bonus_router = Router()
bonus_router.message.middleware(CheckAdmin())


@bonus_router.message(F.text.lower() == 'изменить процент начисления')
async def start_change_bonus(message: Message, state: FSMContext):
    """Запрашиваем новое значение процента"""
    bonus = await get_obj(async_session, BonusPoint, 'name', 'bonus_pointer')
    await message.answer(
        f'Текущий процент начисления составляет {bonus.percent}\n'
        'Введи новое значение используя только цифры',
    )
    await state.update_data(bonus=bonus)
    await state.set_state(BonusForm.percent)


@bonus_router.message(BonusForm.percent)
async def set_new_percent(message: Message, state: FSMContext):
    """проверяем валидность и устанавливаем проценты"""
    if not message.text.isdigit():
        await message.answer('Должны быть только числа')
        return
    percent = int(message.text)
    data = await state.get_data()
    bonus = data.get('bonus')
    bonus.percent = percent
    await state.clear()
    await update_obj(async_session, bonus)
    await message.answer('Проценты изменены')
