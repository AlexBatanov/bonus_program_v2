import os

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from middlewares.user_acces import AccesBot
from keyboards import kb
from db.models import BonusPoint, Buyer, Employee
from db.async_engine import async_session
from utils.crud import get_obj, create_obj
from utils.states import BuyerForm


start_router = Router()
start_router.message.middleware(AccesBot())


@start_router.startup()
async def on_startup():
    """
    Проверяет наличие объекта бонус в бд,
    если нет, то создает.
    Проверяет наличие адина в бд,
    если нет, то создает, tg_id из env.
    
    используется при запуске бота
    """
    tg_id = int(os.getenv('TG_ID'))
    admin = await get_obj(async_session, Employee, 'telegram_id', tg_id)
    obj = await get_obj(async_session, BonusPoint, 'name', 'bonus_pointer')

    if not obj:
        obj = BonusPoint(name='bonus_pointer')
        await create_obj(async_session, obj)
        print("Бонусы добавлены")

    if not admin:
        admin = Employee(
            first_name='Administrator',
            last_name='Admin',
            telegram_id=tg_id,
            is_admin=True,
            is_banned=False
        )
        await create_obj(async_session, admin)


@start_router.message(F.text.lower() == 'начать продажу')
@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext, is_admin: bool):
    """Начало работы бота"""
    await state.clear()
    await state.update_data(is_admin=is_admin)
    if is_admin:
        await message.answer(
            "Введи номер клиента в 11 значном формате.\nПример: 89271112233",
            reply_markup=kb.admin_keys()
        )
    else:
        await message.answer(
            "Введи номер клиента в 11 значном формате.\nПример: 89271112233",
            reply_markup=kb.cancel()
        )

    await state.set_state(BuyerForm.number)


# @start_router.message(F.text.regexp(r"\d{11}"))
@start_router.message(BuyerForm.number, F.text.regexp(r"\d{11}"))
async def check_buyer(message: Message, state: FSMContext, is_admin: bool):
    """
    Проверяем существование покупателя
    Если нет, то переходим к диалогу создания
    иначе открываем диалог работы с клиентом
    """
    await state.update_data(is_admin=is_admin)
    await state.update_data(number=message.text)
    await state.update_data(tg_id=int(message.from_user.id))
    data = await state.get_data()

    buyer = await get_obj(async_session, Buyer, 'number', message.text)
    if buyer:
        await state.update_data(buyer=buyer)
        await message.answer(
            f"Имя: {buyer.name}\n"
            f"Доступно бонусов: {buyer.bonus_points}\n"
            f"Количество установок: {buyer.count_aplications}\n",
            reply_markup=kb.sale_buyer(data.get('is_admin'))
        )
    else:
        await state.update_data(number=message.text)
        await message.answer('Введи имя клиента')
        await state.set_state(BuyerForm.name)


@start_router.message(F.text.lower() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Отменено. Для продолжения работы нажми кнопку "Начать продажу"\U0001F446'
    )