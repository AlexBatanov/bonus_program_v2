from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.update_data import update_data_cheque
from utils.validators import is_valid_data_cheque_buyer
from utils.states import BuyerForm, ChequeForm
from utils.crud import create_obj, get_obj
from db.async_engine import async_session
from db.models import Buyer



buyer_router = Router()

@buyer_router.message(BuyerForm.name)
async def buyer_name(message: Message, state: FSMContext):
    """Устанавлием имя и записываем в бд клиента"""
    await state.update_data(name=message.text)
    data = await state.get_data()
    obj = Buyer(**data)
    await create_obj(async_session, obj)
    await message.answer('Клиент создан')
    await state.clear()


@buyer_router.callback_query(F.data == "saly")
async def input_films(callback: CallbackQuery, state: FSMContext):
    """Устанавливаем состояние пленок для чека"""
    await callback.message.answer('Введи пленки которые установил')
    await state.set_state(ChequeForm.films)
    await callback.answer()


@buyer_router.message(ChequeForm.films)
async def input_amount(message: Message, state: FSMContext):
    """Устанавливем состояние для суммы чека"""
    await state.update_data(films=message.text)
    await message.answer('Введи сумму покупки, только цифры')
    await state.set_state(ChequeForm.amount)


@buyer_router.message(ChequeForm.amount)
async def input_bonus(message: Message, state: FSMContext):
    """Устанавливем состояние для бонусов"""
    await state.update_data(amount=message.text)
    data = await state.get_data()
    buyer = await get_obj(async_session, Buyer, 'number', data.get('number'))
    await state.update_data(buyer=buyer.id)
    await message.answer(
        f'Введи количество бонусов для списания, доступно: {buyer.bonus_points}'
    )
    await state.set_state(BuyerForm.bonus_points)


@buyer_router.message(BuyerForm.bonus_points)
async def chek_data(message: Message, state: FSMContext):
    """Проверяем данные из состояний"""

    await state.update_data(bonus_points=message.text)
    await state.update_data(employee=message.from_user.id)
    data = await state.get_data()
    error_message = await is_valid_data_cheque_buyer(data)
    if error_message:
        await message.answer(error_message)
        return
    cheque_data = update_data_cheque(data)
    print(cheque_data)
    await message.answer(
        f'Установленные пленки: {data.get("films")}\n'
        f'Сумма чека: {data.get("amount")}\n'
        f'Списано баллов: {data.get("bonus_points")}\n\n'
        f'К оплате: {cheque_data.get("amount")}'
    )
    # buyer = await get_obj(async_session, Buyer, 'number', data.get('number'))
    # await message.answer(
    #     f'Введи количество бонусов для списания, доступно: {buyer.bonus_points}'
    # )
    # await state.set_state(BuyerForm.bonus_points)